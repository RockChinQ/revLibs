from typing import Tuple
import logging

from plugins.revLibs.pkg.models.interface import RevLibInterface

from claude_api import Client

import os
import json


class ClaudeImpl(RevLibInterface):

    chatbot: Client = None

    conversation_id: str = None

    @staticmethod
    def create_instance() -> tuple[RevLibInterface, bool, dict]:
        import revcfg
        # 检查claude的cookies是否存在
        if not os.path.exists("claude.json"):
            logging.error("Claude cookies不存在")
            raise Exception("Claude cookies不存在, 请根据文档进行配置: https://github.com/RockChinQ/revLibs")
        
        cookies_list = []
        with open("claude.json", "r", encoding="utf-8") as f:
            cookies_list = json.load(f)
        
        # 把cookies转换为字符串
        cookies = ""

        for cookie in cookies_list:
            cookies += cookie["name"] + "=" + cookie["value"] + ";"

        return ClaudeImpl(cookies), True, cookies_list

    def __init__(self, cookies: str = None):
        self.chatbot = Client(cookies)

    def get_rev_lib_inst(self):
        return self.chatbot

    def get_reply(self, prompt: str, **kwargs) -> Tuple[str, dict]:
        logging.debug("[rev] 请求claude回复: {}".format(prompt))

        if self.conversation_id is None:
            self.conversation_id = self.chatbot.create_new_chat()['uuid']

        resp = self.chatbot.send_message(prompt, self.conversation_id)

        yield resp, {}
    
    def reset_chat(self):
        self.conversation_id = None

    def rollback(self):
        pass
