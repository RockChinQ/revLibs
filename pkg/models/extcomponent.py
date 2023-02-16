from mirai.models.message import MessageComponent

class ForwardMessage(MessageComponent):

    type: str = "Forward"
    nodeList: list

    def __str__(self):
        return "[转发消息]"