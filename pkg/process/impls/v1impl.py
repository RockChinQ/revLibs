from typing import Tuple
from plugins.revLibs.pkg.models.interface import RevLibInterface

from revChatGPT.V1 import Chatbot

import threading

__thr_locks__ = {}


def get_lock(key: str):
    if key not in __thr_locks__:
        __thr_locks__[key] = threading.Lock()
    return __thr_locks__[key]


import logging


class RevChatGPTV1(RevLibInterface):
    """acheong08/ChatGPT的逆向库接口 V1"""
    chatbot: Chatbot = None

    inst_name: str

    @staticmethod
    def create_instance() -> tuple[RevLibInterface, bool, dict]:
        import plugins.revLibs.pkg.accounts.accmgr as accmgr
        valid_acc, acc = accmgr.use_account()
        return RevChatGPTV1(acc), valid_acc, acc

    def __init__(self, cfg):
        logging.debug("[rev] 初始化接口实现，使用账户配置: {}".format(cfg))
        self.chatbot = Chatbot(
            config=cfg,
        )

        self.inst_name = str(cfg)

    def get_rev_lib_inst(self):
        return self.chatbot

    def get_reply(self, prompt: str, **kwargs) -> Tuple[str, dict]:
        import revcfg
        try:
            get_lock(self.inst_name).acquire()
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
            get_lock(self.inst_name).release()

    def reset_chat(self):
        self.chatbot.reset_chat()

    def rollback(self):
        self.chatbot.rollback_conversation()


    
