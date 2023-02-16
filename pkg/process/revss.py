# 逆向库的session
from plugins.revLibs.pkg.models.interface import RevLibInterface

import logging

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

    def __init__(self, name: str):
        self.name = name
        self.__rev_interface_impl__: RevLibInterface = __rev_interface_impl_class__()

    def get_rev_lib_inst(self):
        return self.__rev_interface_impl__.get_rev_lib_inst()

    def get_reply(self, prompt: str, **kwargs) -> str:
        """获取回复"""
        if self.__rev_interface_impl__ is None:
            raise Exception("逆向接口未初始化")
        
        if self.conversation_id is not None:
            kwargs['conversation_id'] = self.conversation_id

        if self.parent_id is not None:
            kwargs['parent_id'] = self.parent_id

        reply_message, reply_dict = self.__rev_interface_impl__.get_reply(prompt, **kwargs)
        self.__ls_prompt__ = prompt

        # logging.debug("revLibs reply: {}".format(reply_dict))

        if self.conversation_id is None:
            self.conversation_id = reply_dict['conversation_id']

        if self.parent_id is None:
            self.parent_id = reply_dict['parent_id']

        return reply_message

    def reset(self):
        """重置会话"""
        self.conversation_id = None
        self.parent_id = None
        self.__rev_interface_impl__.reset_chat()

    def resend(self):
        """重新发送上一条消息"""
        self.__rev_interface_impl__.rollback()
        return self.get_reply(self.__ls_prompt__)

    
def get_session(name: str) -> RevSession:
    """获取session"""
    if name not in __sessions__:
        # 创建session
        __sessions__[name] = RevSession(name)
    return __sessions__[name]