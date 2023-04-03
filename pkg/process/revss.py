# 逆向库的session
from plugins.revLibs.pkg.models.interface import RevLibInterface
from plugins.revLibs.pkg.process.impls.v1impl import RevChatGPTV1
from plugins.revLibs.pkg.process.impls.edgegpt import EdgeGPTImpl
import pkg.openai.dprompt as dprompt
import uuid
import time

import logging
import threading

import config

__sessions__ = {}
"""所有session"""

__rev_interface_impl_class__: RevLibInterface = None

class RevSession:
    name: str

    conversation_id: str = None
    """会话id，第一次获取到回复时生成"""

    parent_id: str = None
    """父会话id"""

    __rev_interface_impl__: RevLibInterface = None

    __ls_prompt__: str = ""

    __set_prompt__: str = ""

    using_account: dict = None

    last_interaction_time: int = 0
    """最后一次交互时间"""

    getting_reply: bool = False

    def __init__(self, name: str):
        self.name = name
        if __rev_interface_impl_class__ is RevChatGPTV1:
            logging.debug("[rev] 逆向接口实现为RevChatGPTV1")
            self.__rev_interface_impl__, valid, acc = __rev_interface_impl_class__.create_instance()
            self.using_account = acc
            self.reset()
        elif __rev_interface_impl_class__ is EdgeGPTImpl:
            logging.debug("[rev] 逆向接口实现为EdgeGPTImpl")
            self.__rev_interface_impl__,_,_ = __rev_interface_impl_class__.create_instance()
            self.reset()

        threading.Thread(target=self.check_expire_loop, daemon=True).start()


    def check_expire_loop(self):
        while True:
            time.sleep(60)
            if self not in __sessions__.values():
                break
            if self.last_interaction_time < int(time.time()) - config.session_expire_time and not self.getting_reply:
                # 删除此session
                logging.info("[rev] 会话 {} 已过期，自动重置".format(self.name))
                del __sessions__[self.name]
                break

    def get_rev_lib_inst(self):
        return self.__rev_interface_impl__.get_rev_lib_inst()

    def get_reply(self, prompt: str, **kwargs) -> str:
        """获取回复"""
        self.getting_reply = True

        if self.__rev_interface_impl__ is None:
            raise Exception("逆向接口未初始化")

        self.last_interaction_time = int(time.time())
        
        self.__ls_prompt__ = prompt
        if self.conversation_id is not None:
            kwargs['conversation_id'] = self.conversation_id
        
        using_name = dprompt.mode_inst().get_using_name()
        dprompt_, _ = dprompt.mode_inst().get_prompt(using_name)
        if self.__set_prompt__ != "":
            dprompt_ = self.__set_prompt__
            self.__set_prompt__ = ""
            
        if dprompt_ != "" and self.conversation_id is None:
            if type(dprompt_) == list:
                dprompt_ = dprompt_[0]['content']
            prompt = dprompt_ +" \n"+ prompt
            logging.info("[rev] 使用情景预设: {}".format(dprompt_))

        # 改成迭代器以支持回复分节
        for reply_period_msg, reply_period_dict in self.__rev_interface_impl__.get_reply(prompt, **kwargs):
            if __rev_interface_impl_class__ is RevChatGPTV1:
                self.conversation_id = reply_period_dict['conversation_id']
            else:
                self.conversation_id = uuid.uuid4().hex
                
            yield reply_period_msg
        
        self.getting_reply = False

    def reset(self, using_prompt_name: str = None) -> str:
        """重置会话"""
        self.conversation_id = None
        self.parent_id = None
        self.__ls_prompt__ = ""
        self.__rev_interface_impl__.reset_chat()
        if using_prompt_name is not None:
            for key in dprompt.get_prompt_dict():
                if key.startswith(using_prompt_name):
                    using_prompt_name = key
                    break
            self.__set_prompt__ = dprompt.get_prompt(using_prompt_name)
            return using_prompt_name

    def resend(self):
        """重新发送上一条消息"""
        self.__rev_interface_impl__.rollback()
        import plugins.revLibs.pkg.process.procmsg as procmsg  # 不优雅的解决办法
        return procmsg.process_message(self.name, self.__ls_prompt__, None, launcher_type=self.name.split("_")[0], launcher_id=int(self.name.split("_")[1]))
        
    
    
def get_session(name: str) -> RevSession:
    """获取session"""
    if name not in __sessions__:
        # 创建session
        __sessions__[name] = RevSession(name)
    return __sessions__[name]
