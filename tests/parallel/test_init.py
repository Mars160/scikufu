import pytest
import time
import asyncio

# 假设你的源码保存在 parallel_utils.py 中
# 如果你的文件名不同，请修改下面的导入
from scikufu.parallel import run_in_parallel, run_async_in_parallel

# ==========================================
# 辅助函数 (Top-level definitions for pickling)
# 多进程模式(ProcessPoolExecutor)需要函数在顶层定义，不能是 lambda 或 内部函数
# ==========================================


def simple_add(a, b):
    return a + b


def slow_square(x, sleep_time=0.1):
    time.sleep(sleep_time)
    return x * x


def fail_sometimes(x, threshold=2):
    # 利用简单的文件标记来模拟重试计数 (因为多进程无法共享内存变量)
    # 在实际测试中，我们会通过控制 args 能够成功
    if x < threshold:
        raise ValueError(f"Value {x} is too small!")
    return x


async def async_simple_add(a, b):
    await asyncio.sleep(0.01)
    return a + b


async def async_fail_sometimes(x, threshold=2):
    if x < threshold:
        raise ValueError("Async fail!")
    return x


# ==========================================
# 测试套件
# ==========================================


class TestRunInParallel:
    def test_single_task_multiple_args_default_backend(self):
        """测试：单个任务函数，多组参数 (默认 backend)"""
        args_list = [(1, 2), (3, 4), (5, 6)]
        results = run_in_parallel(tasks=simple_add, args_=args_list, n_jobs=2)
        assert results == [3, 7, 11]

    def test_multiple_tasks_matching_args(self):
        """测试：多个任务函数，一一对应参数"""
        tasks = [simple_add, simple_add]
        args = [(10, 10), (20, 20)]
        results = run_in_parallel(tasks=tasks, args_=args, n_jobs=2)
        assert results == [20, 40]

    def test_threading_backend(self):
        """测试：多线程模式 (thread=True)"""
        args = [(i,) for i in range(5)]
        results = run_in_parallel(
            tasks=slow_square,
            args_=args,
            thread=True,
            n_jobs=5,
            kwargs_=[{"sleep_time": 0.1}] * 5,
        )
        # 0, 1, 4, 9, 16
        assert results == [0, 1, 4, 9, 16]

    def test_multiprocessing_backend(self):
        """测试：多进程模式 (process=True)"""
        # 注意：这里必须使用顶层定义的 simple_add
        args = [(i, 1) for i in range(5)]
        results = run_in_parallel(tasks=simple_add, args_=args, process=True, n_jobs=2)
        assert results == [1, 2, 3, 4, 5]

    def test_keep_order_true(self):
        """测试：保持顺序 (keep_order=True)"""
        # 第一个任务睡得久，第二个睡得短
        # 如果不保持顺序，结果应该是 [1, 0]
        # 保持顺序应该是 [0, 1]
        tasks = [slow_square, slow_square]
        args = [(0,), (1,)]
        kwargs = [{"sleep_time": 0.5}, {"sleep_time": 0.1}]

        start_t = time.time()
        results = run_in_parallel(
            tasks=tasks,
            args_=args,
            kwargs_=kwargs,
            n_jobs=2,
            keep_order=True,
            thread=True,
        )
        end_t = time.time()

        assert results == [0, 1]
        # 确保是并行运行的 (时间应该小于 sum(0.5 + 0.1))
        assert (end_t - start_t) < 0.55

    def test_keep_order_false(self):
        """测试：不保持顺序 (keep_order=False)"""
        tasks = [slow_square, slow_square]
        # 任务0: 慢, 任务1: 快
        args = [(10,), (20,)]
        kwargs = [{"sleep_time": 0.5}, {"sleep_time": 0.1}]

        results = run_in_parallel(
            tasks=tasks,
            args_=args,
            kwargs_=kwargs,
            n_jobs=2,
            keep_order=False,
            thread=True,
        )

        # 因为任务1快，它应该先完成并被 append 到列表
        # 期望结果: [400, 100] 而不是 [100, 400]
        assert results == [400, 100]

    def test_caching(self, tmp_path):
        """测试：缓存功能"""
        cache_dir = tmp_path / "cache_test"

        # 定义一个带副作用的函数来验证是否命中缓存
        # 由于多进程难以检测副作用，我们使用 Thread 或 Async 模式，
        # 并使用一个可变对象 (list) 来记录调用次数
        call_counter = []

        def side_effect_add(a, b):
            call_counter.append(1)
            time.sleep(0.1)
            return a + b

        # 第一次运行：应该调用函数，并写入缓存
        res1 = run_in_parallel(
            tasks=side_effect_add,
            args_=[(1, 1)],
            cache_dir=cache_dir,
            n_jobs=1,
            thread=True,  # 使用线程以共享 call_counter
        )
        assert res1 == [2]
        assert len(call_counter) == 1

        # 第二次运行：应该读取缓存，不增加 call_counter
        res2 = run_in_parallel(
            tasks=side_effect_add,
            args_=[(1, 1)],
            cache_dir=cache_dir,
            n_jobs=1,
            thread=True,
        )
        assert res2 == [2]
        assert len(call_counter) == 1  # 计数器未增加，说明命中了缓存

    def test_retry_mechanism(self):
        """测试：重试机制"""

        # 为了测试重试，我们构造一个闭包或类实例来维护状态
        class FlakyTask:
            def __init__(self):
                self.attempts = 0

            def run(self, x):
                self.attempts += 1
                if self.attempts < 3:
                    raise ValueError("Not yet!")
                return x

        flaky = FlakyTask()

        # 设置 retries=3，足以覆盖2次失败
        results = run_in_parallel(
            tasks=flaky.run,
            args_=[(100,)],
            retries=3,
            retry_delay=0.01,
            n_jobs=1,
            thread=True,  # 使用线程以共享 flaky 实例状态
        )
        assert results == [100]
        assert flaky.attempts == 3

    def test_exception_propagation(self):
        """测试：超过重试次数后抛出异常"""

        def always_fail():
            raise RuntimeError("Doom")

        with pytest.raises(RuntimeError, match="Doom"):
            run_in_parallel(tasks=always_fail, retries=1, retry_delay=0.01)

    def test_argument_mismatch_error(self):
        """测试：参数长度不匹配抛出 ValueError"""
        with pytest.raises(ValueError, match="args_ length"):
            run_in_parallel(
                tasks=[simple_add, simple_add],
                args_=[(1,)],  # 只有1组参数，但有2个任务
            )


class TestRunAsyncInParallel:
    def test_async_basic(self):
        """测试：基本的 Async 任务"""
        results = run_async_in_parallel(tasks=async_simple_add, args_=[(1, 2), (3, 4)])
        assert results == [3, 7]

    def test_async_caching(self, tmp_path):
        """测试：Async 缓存"""
        cache_dir = tmp_path / "async_cache"

        counter = {"count": 0}

        async def counted_add(a, b):
            counter["count"] += 1
            return a + b

        # 第一次运行
        run_async_in_parallel(tasks=counted_add, args_=[(10, 10)], cache_dir=cache_dir)
        assert counter["count"] == 1

        # 第二次运行 (命中缓存)
        res = run_async_in_parallel(
            tasks=counted_add, args_=[(10, 10)], cache_dir=cache_dir
        )
        assert res == [20]
        assert counter["count"] == 1  # 没有再次执行

    def test_async_retry(self):
        """测试：Async 重试"""

        class AsyncFlaky:
            def __init__(self):
                self.calls = 0

            async def run(self):
                self.calls += 1
                if self.calls < 3:
                    raise ValueError("Fail")
                return "Success"

        flaky = AsyncFlaky()
        res = run_async_in_parallel(tasks=flaky.run, retries=5, retry_delay=0.01)
        assert res == ["Success"]
        assert flaky.calls == 3

    def test_async_unsupported_options(self):
        """测试：Async 模式不支持 thread/process 参数"""
        with pytest.raises(AssertionError):
            run_async_in_parallel(tasks=async_simple_add, thread=True)


if __name__ == "__main__":
    # 允许直接运行此脚本进行测试
    pytest.main([__file__])
