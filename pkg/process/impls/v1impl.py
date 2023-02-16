from typing import Tuple
from plugins.revLibs.pkg.models.interface import RevLibInterface

from revChatGPT.V1 import Chatbot

import threading
__thr_lock__: threading.Lock = threading.Lock()

import logging

class RevChatGPTV1(RevLibInterface):
    """acheong08/ChatGPT的逆向库接口 V1"""
    chatbot: Chatbot = None

    def __init__(self):
        import revcfg
        self.chatbot = Chatbot(
            config=revcfg.openai_account
        )

    def get_reply(self, prompt: str, **kwargs) -> Tuple[str, dict]:
        try:
            __thr_lock__.acquire()
            if self.chatbot is None:
                raise Exception("acheong08/ChatGPT.V1 逆向接口未初始化")
            
            reply_gen = self.chatbot.ask(prompt, **kwargs)
            reply = {}

            logging.debug("已响应，正在接收...")

            for r in reply_gen:
                reply = r

            logging.debug("接收完毕: {}".format(reply))

            return reply['message'], reply
        finally:
            __thr_lock__.release()

    def reset_chat(self):
        self.chatbot.reset_chat()

    def rollback(self):
        self.chatbot.rollback_conversation()