from typing import Tuple
import logging

from plugins.revLibs.pkg.models.interface import RevLibInterface

from bardapi import Bard

import os
import json


class BardImpl(RevLibInterface):

    chatbot: Bard = None

    token: str = None

    @staticmethod
    def create_instance() -> tuple[RevLibInterface, bool, dict]:
        import revcfg
        # 检查bard的cookies是否存在
        if not os.path.exists("bard.json"):
            logging.error("Bard cookies不存在")
            raise Exception("Bard cookies不存在, 请根据文档进行配置: https://github.com/RockChinQ/revLibs")

        cookies_list = []
        with open("bard.json", "r", encoding="utf-8") as f:
            cookies_list = json.load(f)

        return BardImpl(cookies_list), True, cookies_list

    def __init__(self, cookies: str = None):

        __Secure_1PSID = ""

        for cookie in cookies:
            if cookie["name"] == "__Secure-1PSID":
                __Secure_1PSID = cookie["value"]
                break

        if __Secure_1PSID == "":
            raise Exception("Bard cookies中不含有所需的__Secure-1PSID字段, 请尝试重新获取.")

        self.token = __Secure_1PSID

        self.chatbot = Bard(token=__Secure_1PSID)

    def get_rev_lib_inst(self):
        return self.chatbot

    def get_reply(self, prompt: str, **kwargs) -> Tuple[str, dict]:
        logging.debug("[rev] 请求bard回复: {}".format(prompt))

        resp = self.chatbot.get_answer(prompt)

        yield resp['content'], resp

    def reset_chat(self):
        self.chatbot = Bard(token=self.token)

    def rollback(self):
        pass
