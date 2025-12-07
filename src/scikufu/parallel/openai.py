import src.scikufu.parallel
import openai
import os


from typing import Iterable, Optional, Union


class Client:
    def __init__(self, api_key: str, base_url: str = "https://api.openai.com/v1"):
        self.api_key = api_key
        self.base_url = base_url
        self.OpenAI = openai.AsyncOpenAI(api_key=self.api_key, base_url=self.base_url)

    def chat_completion(
        self,
        messages: Iterable[Iterable[openai.types.chat.ChatCompletionMessageParam]],
        model: Union[str, Iterable[str]],
        cache_dir: Optional[os.PathLike] = None,
        n_jobs: int = 4,
        with_tqdm: bool = True,
        retries: int = 0,
        retry_delay: float = 1.0,
        keep_order: bool = True,
        **kwargs,
    ):
        models = model if isinstance(model, Iterable) else [model] * len(messages)

        async def make_task(msg, model):
            return await self.OpenAI.chat.completions.create(
                model=model,
                messages=msg,
                **kwargs,
            )

        args_ = []
        kwargs_ = []
        for msg, mdl in zip(messages, models):
            args_.append((msg, mdl))
            kwargs_.append(kwargs)

        return src.scikufu.parallel.run_async_in_parallel(
            make_task,
            args_=args_,
            kwargs_=kwargs_,
            n_jobs=n_jobs,
            with_tqdm=with_tqdm,
            cache_dir=cache_dir,
            retries=retries,
            retry_delay=retry_delay,
            keep_order=keep_order,
        )
