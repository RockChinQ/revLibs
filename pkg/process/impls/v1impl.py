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

    def get_rev_lib_inst(self):
        return self.chatbot

    def get_reply(self, prompt: str, **kwargs) -> Tuple[str, dict]:
        import revcfg
        try:
            __thr_lock__.acquire()
            if self.chatbot is None:
                raise Exception("acheong08/ChatGPT.V1 逆向接口未初始化")
            
            reply_gen = self.chatbot.ask(prompt, **kwargs)
            already_reply_msg = ""
            reply = {}

            first_received = False
            for r in reply_gen:
                if not first_received:
                    first_received = True
                    logging.debug("已响应，正在接收...")
                reply = r

                if "message" in reply:
                    assert isinstance(reply['message'], str)
                    reply['message'] = reply['message'].replace(already_reply_msg, "")

                # 判断是否达到分节长度
                if "message" in reply and len(reply['message']) >= revcfg.blog_msg_threshold:
                    yield reply['message'], reply
                    already_reply_msg += reply['message']
                    reply = {}

            logging.debug("接收完毕: {}".format(reply))

            yield reply['message'], reply
        except Exception as e:
            raise e
        finally:
            __thr_lock__.release()

    def reset_chat(self):
        self.chatbot.reset_chat()

    def rollback(self):
        self.chatbot.rollback_conversation()