import scikufu.parallel

import openai.types.chat as libopenai_chat
import openai as libopenai

import os


from typing import Iterable, Optional, Union, TypeVar
from pydantic import BaseModel

T = TypeVar("T")


class Client:
    def __init__(self, api_key: str, base_url: str = "https://api.openai.com/v1"):
        self.api_key = api_key
        self.base_url = base_url
        self.OpenAI = libopenai.AsyncOpenAI(
            api_key=self.api_key, base_url=self.base_url
        )

        print(f"Initialized OpenAI Client with base_url: {self.base_url}")

    def chat_completion(
        self,
        messages: Iterable[Iterable[libopenai_chat.ChatCompletionMessageParam]],
        model: Union[str, Iterable[str]],
        cache_dir: Optional[os.PathLike] = None,
        n_jobs: int = 4,
        with_tqdm: bool = True,
        retries: int = 0,
        retry_delay: float = 1.0,
        keep_order: bool = True,
        **kwargs,
    ):
        models = [model] * len(messages) if isinstance(model, str) else model

        async def make_task(msg, model, **kwargs):
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

        return scikufu.parallel.run_async_in_parallel(
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

    def chat_completion_parse(
        self,
        messages: Iterable[Iterable[libopenai.types.chat.ChatCompletionMessageParam]],
        model: Union[str, Iterable[str]],
        response_format: type[T],
        cache_dir: Optional[os.PathLike] = None,
        n_jobs: int = 4,
        with_tqdm: bool = True,
        retries: int = 0,
        retry_delay: float = 1.0,
        keep_order: bool = True,
        **kwargs,
    ):
        # check that T is a subclass of BaseModel
        assert issubclass(response_format, BaseModel), (
            "T must be a subclass of pydantic.BaseModel"
        )

        models = [model] * len(messages) if isinstance(model, str) else model

        async def make_task(msg, model, **kwargs):
            return await self.OpenAI.chat.completions.parse(
                model=model,
                messages=msg,
                response_format=response_format,
                **kwargs,
            )

        args_ = []
        kwargs_ = []
        for msg, mdl in zip(messages, models):
            args_.append((msg, mdl))
            kwargs_.append(kwargs)

        return scikufu.parallel.run_async_in_parallel(
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
