from typing import Tuple
import logging

from plugins.revLibs.pkg.models.interface import RevLibInterface

from hugchat import hugchat

import os
import json


class HugChatImpl(RevLibInterface):

    chatbot: hugchat.ChatBot = None

    @staticmethod
    def create_instance() -> tuple[RevLibInterface, bool, dict]:
        import revcfg
        # 检查hugging chat的cookies是否存在
        if not os.path.exists("hugchat.json"):
            logging.error("HuggingChat cookies不存在")
            raise Exception("HuggingChat cookies不存在, 请根据文档进行配置: https://github.com/RockChinQ/revLibs")
        
        cookies_dict = {}
        with open("hugchat.json", "r", encoding="utf-8") as f:
            cookies_dict = json.load(f)
        return HugChatImpl(cookies_dict), True, cookies_dict

    def __init__(self, cookies_dict: dict = None):
        self.chatbot = hugchat.ChatBot(cookies=cookies_dict)

    def get_rev_lib_inst(self):
        return self.chatbot

    def get_reply(self, prompt: str, **kwargs) -> Tuple[str, dict]:
        logging.debug("[rev] 请求回复: {}".format(prompt))

        resp = self.chatbot.chat(prompt)

        yield resp, {}

    def reset_chat(self):
        self.chatbot.new_conversation()

    def rollback(self):
        pass

