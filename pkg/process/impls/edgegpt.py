"""接入acheone08/EdgeGPT
"""
import os
import logging
import json
import asyncio

from plugins.revLibs.pkg.models.interface import RevLibInterface
from EdgeGPT import Chatbot, ConversationStyle


ref_num_loop = ['¹', '²', '³', '⁴', '⁵', '⁶', '⁷', '⁸', '⁹', '¹⁰', '¹¹', '¹²', '¹³', '¹⁴', '¹⁵', '¹⁶', '¹⁷', '¹⁸', '¹⁹', '²⁰']


class EdgeGPTImpl(RevLibInterface):
    """使用acheong08/EdgeGPT接入new bing
    """
    chatbot: Chatbot = None

    style = ConversationStyle.balanced

    inst_name: str

    @staticmethod
    def create_instance() -> tuple[RevLibInterface, bool]:
        import revcfg

        return EdgeGPTImpl(revcfg.new_bing_style if hasattr(revcfg, "new_bing_style") else ConversationStyle.balanced), True

    def __init__(self, style):
        # logging.debug("[rev] 初始化接口实现，使用账户cookies: {}".format(str(cookies)[:30]))
        logging.debug("[rev] 初始化New Bing接口实现")
        self.chatbot = Chatbot()
        self.style = style
        # 随机一个uuid作为实例名
        import uuid
        self.inst_name = str(uuid.uuid4())
    
    def get_rev_lib_inst(self):
        return self.chatbot

    def get_reply(self, prompt: str, **kwargs) -> tuple[str, dict]:
        """获取回复"""
        logging.debug("[rev] 请求回复: {}".format(prompt))
        task = self.chatbot.ask(prompt, conversation_style=self.style)
        resp = asyncio.run(task)
        logging.debug(json.dumps(resp, indent=4, ensure_ascii=False))

        reply_obj = resp["item"]["messages"][-1] if 'messageType' not in resp["item"]["messages"][-1] else resp["item"]["messages"][-2]
        body = reply_obj["text"] if "text" in reply_obj else (
            reply_obj['hiddenText'] if "hiddenText" in reply_obj else (
                reply_obj['spokenText'] if "spokenText" in reply_obj else ""
            )
        )

        if "sourceAttributions" in reply_obj:
            refs_str = "参考资料: \n"
            index = 1
            for ref in reply_obj["sourceAttributions"]:
                refs_str += "{}".format(ref_num_loop[index-1]) + " " + ref['providerDisplayName'] + " | " + ref['seeMoreUrl'] + "\n"
                index += 1

            throttling = resp["item"]["throttling"]

            throttling_str = "本次对话: {}/{}".format(throttling["numUserMessagesInConversation"], throttling["maxNumUserMessagesInConversation"])
            
            import revcfg
            if hasattr(revcfg, "output_references") and not revcfg.output_references:
                # 把正文的[^n^]替换成空
                import re
                body = re.sub(r"\[\^[0-9]+\^\]", "", body)
            else:
                # 把正文的[^n^]替换成对应的序号
                for i in range(index):
                    body = body.replace("[^"+str(i+1)+"^]", ref_num_loop[i])

            # if throttling["numUserMessagesInConversation"] == 3:
            if throttling["numUserMessagesInConversation"] == throttling["maxNumUserMessagesInConversation"]:
                self.reset_chat()
                throttling_str += "(已达最大次数，下一回合将开启新对话)"

            reply_str = body + "\n\n" + ((refs_str + "\n\n") if index != 1 and (not hasattr(revcfg, "output_references") or revcfg.output_references) else "") + throttling_str
            
            yield reply_str, resp
        else:
            self.reset_chat()
            yield "err: 可能由于内容不当，对话已被接口拒绝，下一回合将开启新的会话。", resp

    def reset_chat(self):
        asyncio.run(self.chatbot.reset())

    def rollback(self):
        pass