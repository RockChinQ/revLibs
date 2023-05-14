from typing import Tuple
import logging

from plugins.revLibs.pkg.models.interface import RevLibInterface

from hugchat import hugchat


class HugChatImpl(RevLibInterface):

    chatbot: hugchat.ChatBot = None

    @staticmethod
    def create_instance() -> tuple[RevLibInterface, bool, dict]:
        import revcfg
        return HugChatImpl(), True, {}

    def __init__(self):
        self.chatbot = hugchat.ChatBot()

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

