from typing import Tuple
import logging

from plugins.revLibs.pkg.models.interface import RevLibInterface

import g4f
from g4f import models


class GPT4FreeImpl(RevLibInterface):

    messages: list[dict]

    use_model: models.Model = models.gpt_4

    use_provider: g4f.Provider.BaseProvider = None

    @staticmethod
    def create_instance() -> tuple[RevLibInterface, bool, dict]:
        return GPT4FreeImpl(), True, {}

    @classmethod
    def select_provider(cls):
        logging.info("[rev] 测试并选择provider，如果某个provider测试过久，可以在revcfg.py中将其排除")

        from g4f.Provider import __all__ as providers

        providers = providers.copy()

        exclude = [
            'Acytoo'
        ]

        import revcfg
        
        if hasattr(revcfg, 'g4f_use_adapters') and len(revcfg.g4f_use_adapters) > 0:
            providers = revcfg.g4f_use_adapters
            logging.debug("[rev] 已指定provider列表: {}".format(providers))

        if hasattr(revcfg, 'g4f_exclude_adapters') and len(revcfg.g4f_exclude_adapters) > 0:
            exclude = revcfg.g4f_exclude_adapters
            logging.debug("[rev] 已指定排除provider列表: {}".format(exclude))

        for provider in providers:

            if provider in exclude:
                continue

            logging.info("[rev] 测试provider: {}".format(provider))
            provider = getattr(g4f.Provider, provider)
            try:
                response = g4f.ChatCompletion.create(
                    model=cls.use_model,
                    messages=[
                        {
                            "role": "user",
                            "content": "hi"
                        }
                    ],
                    provider=provider
                )

                logging.debug("[rev] 测试provider: {} 成功: {}".format(provider, response))
                cls.use_provider = provider
                break
            except Exception as e:
                continue

    def __init__(self):
        self.messages = []

        if GPT4FreeImpl.use_provider is None:
            # 测试可用模型
            self.select_provider()

    def get_rev_lib_inst(self):
        return None

    def get_reply(self, prompt: str, **kwargs) -> Tuple[str, dict]:
        logging.debug("[rev] 请求gpt4free: {} 回复: {}".format(GPT4FreeImpl.use_provider, prompt))

        retry = 0
        while True:
            try:
                resp = g4f.ChatCompletion.create(
                    model=GPT4FreeImpl.use_model,
                    messages=self.messages+[
                        {
                            "role": "user",
                            "content": prompt
                        }
                    ],
                    provider=GPT4FreeImpl.use_provider,
                )
                
                self.messages.append(
                    {
                        "role": "user",
                        "content": prompt
                    }
                )
                self.messages.append(
                    {
                        "role": "assistant",
                        "content": resp
                    }
                )

                yield resp, {}
                break
            except Exception as e:
                retry += 1

                if retry >= 3:
                    raise e
                
                GPT4FreeImpl.select_provider()

    def reset_chat(self):
        self.messages = []

    def rollback(self):

        if len(self.messages) < 2:
            return

        self.messages.pop()
        self.messages.pop()