from typing import Tuple
from plugins.revLibs.pkg.models.interface import RevLibInterface

from revChatGPT.V1 import Chatbot

class RevChatGPTV1(RevLibInterface):
    """acheong08/ChatGPT的逆向库接口 V1"""
    chatbot: Chatbot = None

    def __init__(self):
        import revcfg
        self.chatbot = Chatbot(
            config=revcfg.openai_account
        )

    def get_reply(self, prompt: str, **kwargs) -> Tuple[str, dict]:
        if self.chatbot is None:
            raise Exception("acheong08/ChatGPT.V1 逆向接口未初始化")
        
        reply_gen = self.chatbot.ask(prompt, **kwargs)
        reply = {}

        for r in reply_gen:
            reply = r

        return reply['message'], reply
