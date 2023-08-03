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
        logging.debug("[rev] 请求ChatGPT回复: {}".format(prompt))

        # 构建函数代理
        funcs = []

        import pkg.plugin.models as models
        import pkg.plugin.host as plugin_host
        import pkg.openai.funcmgr as funcmgr
        if hasattr(models, "require_ver"):
            funcs = funcmgr.get_func_schema_list()
            for func in funcs:
                func['function'] = plugin_host.__function_inst_map__[func['name']]
        
        from .fproxy import Proxy

        fp = Proxy(funcs)

        try:
            get_lock(self.inst_name).acquire()
            if self.chatbot is None:
                raise Exception("acheong08/ChatGPT.V1 逆向接口未初始化")

            prompt = fp.prompt(prompt)
            
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

            logging.debug("接收完毕: {}".format(reply))

            # 检查是否有JSON函数调用
            is_func_call, func_name, args = fp.extra_function_call(reply['message'])

            while is_func_call:
                logging.info("[REV] 执行函数调用: {} {}".format(func_name, args))
                
                result = ""

                try:
                    result = fp.call(func_name, args)
                    logging.debug("func result: {}".format(result))
                    logging.info("[REV] 函数调用完成。")
                except Exception as e:
                    logging.info("[REV] 函数调用失败。")
                    result = "error: failed to call function: "+str(e)
                
                reply = {}

                for data in self.chatbot.ask(
                    prompt="Function call result: "+result
                ):
                    try:
                        assert 'message' in data
                        reply = data
                    except:
                        continue

                logging.debug("ChatGPT's output: {}".format(reply['message']))

                is_func_call, func_name, args = fp.extra_function_call(reply['message'])

            yield reply['message'], reply
        except Exception as e:
            raise e
        finally:
            get_lock(self.inst_name).release()

    def reset_chat(self):
        self.chatbot.reset_chat()

    def rollback(self):
        self.chatbot.rollback_conversation()


    
