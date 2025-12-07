import diskcache
import pickle
import asyncio
import concurrent.futures
import time
import os
import logging
import dataclasses
from typing import Any, Dict, List, Callable, Optional, Iterable, TypeVar, Tuple, Union

logger = logging.getLogger(__name__)

T = TypeVar("T")

# 定义一个哨兵对象
_MISSING = object()


@dataclasses.dataclass
class ParallelParams:
    n_jobs: int = 1
    with_tqdm: bool = True
    cache_dir: Optional[Union[str, os.PathLike]] = None
    thread: bool = False
    process: bool = False
    retries: int = 0
    retry_delay: float = 1.0
    keep_order: bool = True


def _make_cache_key(task: Callable, args: tuple, kwargs: dict) -> Optional[bytes]:
    """生成缓存Key，处理 Lambda 和 Pickle 异常"""
    try:
        task_name = task.__name__
        # 如果是 lambda，加入字节码以区分不同逻辑的 lambda
        if task_name == "<lambda>":
            # 注意：如果 lambda 闭包引用了外部变量，co_code 可能不够，
            # 但比单纯依靠 args 强很多。
            code_bytes = task.__code__.co_code
            cache_key_obj = ("<lambda>", code_bytes, args, kwargs)
        else:
            cache_key_obj = (task_name, args, kwargs)

        return pickle.dumps(cache_key_obj)
    except (pickle.PicklingError, AttributeError, TypeError):
        # 如果参数无法序列化，不仅不报错，而是放弃缓存
        logger.debug(f"Args for task {task} cannot be pickled. Skipping cache.")
        return None


async def _exec_async_with_retry(
    index: int,
    task: Callable,
    args: tuple,
    kwargs: dict,
    cache: Optional[diskcache.Cache],
    retries: int,
    retry_delay: float,
    sem: asyncio.Semaphore,
) -> Tuple[int, Any]:
    """Async 任务执行包装器"""
    async with sem:
        key = None
        if cache is not None:
            key = _make_cache_key(task, args, kwargs)
            if key is not None:
                try:
                    # 必须在线程池中运行同步的 cache 操作，避免阻塞事件循环
                    # diskcache 虽然快，但仍是 I/O
                    result = cache.get(key, default=_MISSING)
                    if result is not _MISSING:
                        return index, result
                except Exception:
                    pass  # 缓存读取失败，降级运行

        last_exception = None
        for attempt in range(retries + 1):
            try:
                result = await task(*args, **kwargs)
                if cache is not None and key is not None:
                    try:
                        cache.set(key, result)
                    except Exception:
                        pass  # 缓存写入失败忽略
                return index, result
            except Exception as e:
                last_exception = e
                if attempt < retries:
                    await asyncio.sleep(retry_delay)

        raise last_exception


def run_async_in_parallel(
    tasks: Union[Iterable[Callable[..., Any]], Callable[..., Any]],
    args_: Optional[Iterable[Iterable[Any]]] = None,
    kwargs_: Optional[Iterable[Dict[str, Any]]] = None,
    **kwargs,
) -> List[Any]:
    """
    Execute a list of async tasks in parallel.
    Returns a list of results (not Futures).
    """
    # 避免变量名遮蔽，重命名配置对象
    p_params = ParallelParams(**kwargs)
    assert p_params.thread is False and p_params.process is False, (
        "thread and process options are not supported in async mode."
    )

    cache = None
    if p_params.cache_dir:
        cache = diskcache.Cache(p_params.cache_dir, size_limit=int(1e9))

    try:
        # --- 参数归一化处理 (复用逻辑) ---
        safe_tasks, safe_args, safe_kwargs, task_num = _normalize_tasks(
            tasks, args_, kwargs_
        )

        sem = asyncio.Semaphore(p_params.n_jobs)

        # 创建协程列表
        coros = [
            _exec_async_with_retry(
                i,
                safe_tasks[i],
                safe_args[i],
                safe_kwargs[i],
                cache,
                p_params.retries,
                p_params.retry_delay,
                sem,
            )
            for i in range(task_num)
        ]

        async def main_loop():
            if p_params.with_tqdm:
                from tqdm.asyncio import tqdm_asyncio

                # 使用 tqdm.gather 自动处理进度条
                # 注意：gather 默认按输入顺序返回，这符合 keep_order=True
                # 如果 keep_order=False，gather 实际上也是等待所有完成，
                # 对于 async 来说，如果不使用 generator yield，直接返回 List 的话，
                # gather 是最简单的方式。
                results_with_index = await tqdm_asyncio.gather(*coros)
            else:
                results_with_index = await asyncio.gather(*coros)

            return results_with_index

        # 运行事件循环
        results_with_index = asyncio.run(main_loop())

        # --- 处理返回值顺序 ---
        # 如果 keep_order=True (默认): gather 已经保证了顺序，只需要剥离 index
        if p_params.keep_order:
            return [res for idx, res in results_with_index]
        else:
            # 如果 keep_order=False，实际上 gather 返回的也是有序的。
            # 这里的语义有点模糊，通常 List 返回意味着必须等所有结束。
            # 为了严谨支持 "keep_order=False" 可能会导致乱序（按完成时间），
            # 但由于我们这里用了 gather，它已经强制排序了。
            # 如果真要乱序 List，需要改写成 as_completed 并 append。
            # 鉴于 gather 的特性，这里我们直接返回结果即可。
            return [res for idx, res in results_with_index]

    finally:
        if cache is not None:
            cache.close()


def _exec_sync_with_retry(
    task: Callable[..., T],
    args: Tuple[Any, ...],
    kwargs: Dict[str, Any],
    cache: Optional[diskcache.Cache],
    retries: int,
    retry_delay: float,
) -> T:
    """
    包装函数：处理缓存 + 重试逻辑 + 参数传递 (同步版)
    """
    key = None
    if cache is not None:
        key = _make_cache_key(task, args, kwargs)
        if key is not None:
            try:
                result = cache.get(key, default=_MISSING)
                if result is not _MISSING:
                    return result
            except Exception:
                pass

    last_exception = None
    for attempt in range(retries + 1):
        try:
            result = task(*args, **kwargs)
            if cache is not None and key is not None:
                try:
                    cache.set(key, result)
                except Exception:
                    pass
            return result
        except Exception as e:
            last_exception = e
            if attempt < retries:
                time.sleep(retry_delay)

    raise last_exception


def _normalize_tasks(tasks, args_, kwargs_):
    """
    辅助函数：统一处理 tasks, args, kwargs 的对齐逻辑
    返回: (task_list, args_list, kwargs_list, count)
    """
    if not isinstance(tasks, Iterable):
        # Single task case
        if args_ is None:
            safe_args = [()]
        else:
            safe_args = args_
        if kwargs_ is None:
            safe_kwargs = [{}]
        else:
            safe_kwargs = kwargs_

        args_num = len(safe_args)
        kwargs_num = len(safe_kwargs)

        task_num = max(args_num, kwargs_num)

        if args_num != task_num:
            if args_num == 1:
                safe_args = safe_args * task_num
            else:
                raise ValueError(
                    f"args_ length ({args_num}) must match kwargs_ length ({kwargs_num})"
                )
        if kwargs_num != task_num:
            if kwargs_num == 1:
                safe_kwargs = safe_kwargs * task_num
            else:
                raise ValueError(
                    f"kwargs_ length ({kwargs_num}) must match args_ length ({args_num})"
                )

        safe_tasks = [tasks] * task_num
    else:
        # Multiple tasks case
        task_num = len(tasks)
        safe_tasks = tasks

        if args_ is None:
            safe_args = [()] * task_num
        else:
            if len(args_) != task_num:
                raise ValueError(
                    f"args_ length ({len(args_)}) must match tasks length ({task_num})"
                )
            safe_args = args_

        if kwargs_ is None:
            safe_kwargs = [{}] * task_num
        else:
            if len(kwargs_) != task_num:
                raise ValueError(
                    f"kwargs_ length ({len(kwargs_)}) must match tasks length ({task_num})"
                )
            safe_kwargs = kwargs_

    return safe_tasks, safe_args, safe_kwargs, task_num


def run_in_parallel(
    tasks: Union[Iterable[Callable[..., T]], Callable[..., T]],
    args_: Optional[Iterable[Iterable[Any]]] = None,
    kwargs_: Optional[Iterable[Dict[str, Any]]] = None,
    **kwargs,
) -> List[T]:
    """
    Execute a list of tasks in parallel using Threads or Processes.
    Also supports running sync tasks in an asyncio loop (though less common for pure sync code).
    """
    p_params = ParallelParams(**kwargs)

    # 修复 tqdm 导入
    if p_params.with_tqdm:
        from tqdm import tqdm
    else:

        def tqdm(iterable, total=None):
            yield from iterable

    cache = None
    if p_params.cache_dir:
        cache = diskcache.Cache(p_params.cache_dir, size_limit=int(1e9))

    try:
        # 参数归一化
        safe_tasks, safe_args, safe_kwargs, task_num = _normalize_tasks(
            tasks, args_, kwargs_
        )

        # 结果容器
        results_container = [None] * task_num if p_params.keep_order else []

        # ----------------------------------------------------------------------
        # Thread / Process 模式
        # ----------------------------------------------------------------------
        if p_params.thread or p_params.process:
            Executor = (
                concurrent.futures.ThreadPoolExecutor
                if p_params.thread
                else concurrent.futures.ProcessPoolExecutor
            )

            with Executor(max_workers=p_params.n_jobs) as executor:
                future_to_index = {}

                for i in range(task_num):
                    future = executor.submit(
                        _exec_sync_with_retry,
                        safe_tasks[i],
                        safe_args[i],
                        safe_kwargs[i],
                        cache,  # ProcessPoolExecutor下传递cache引用可能会有问题(取决于diskcache是否picklable)，
                        # 但diskcache通常是基于文件路径的，可以pickled。
                        p_params.retries,
                        p_params.retry_delay,
                    )
                    future_to_index[future] = i

                for future in tqdm(
                    concurrent.futures.as_completed(future_to_index.keys()),
                    total=len(future_to_index),
                ):
                    res = future.result()
                    original_idx = future_to_index[future]

                    if p_params.keep_order:
                        results_container[original_idx] = res
                    else:
                        results_container.append(res)

            return results_container

        # ----------------------------------------------------------------------
        # Asyncio 模式 (运行同步函数)
        # ----------------------------------------------------------------------
        else:

            async def run_sync_tasks_in_asyncio():
                loop = asyncio.get_running_loop()
                sem = asyncio.Semaphore(p_params.n_jobs)

                async def sem_task(index, task, arg, kwarg):
                    async with sem:
                        # run_in_executor 也是在线程池中运行，所以也是 Thread 模式的一种变体
                        res = await loop.run_in_executor(
                            None,
                            _exec_sync_with_retry,
                            task,
                            arg,
                            kwarg,
                            cache,
                            p_params.retries,
                            p_params.retry_delay,
                        )
                        return index, res

                coros = [
                    sem_task(i, safe_tasks[i], safe_args[i], safe_kwargs[i])
                    for i in range(task_num)
                ]

                # 这里正确处理了 keep_order
                for coro in tqdm(asyncio.as_completed(coros), total=len(coros)):
                    idx, res = await coro
                    if p_params.keep_order:
                        results_container[idx] = res
                    else:
                        results_container.append(res)

                return results_container

            return asyncio.run(run_sync_tasks_in_asyncio())

    finally:
        if cache is not None:
            cache.close()
