import plugins.revLibs.pkg.process.revss as revss

def process_command(session_name: str, **kwargs) -> str:
    """处理命令"""

    cmd = kwargs['command']
    params = kwargs['params']

    session: revss.RevSession = revss.get_session(session_name)

    reply_message = ""

    if cmd == 'reset':
        session.reset()
        reply_message = "已重置会话"
    elif cmd == 'list':
        pass
    elif cmd == 'prompt':
        reply_message = "正在使用逆向库插件，暂不支持查看对话前文。"
    elif cmd == "last":
        pass
    elif cmd == "next":
        pass
    elif cmd == "resend":
        reply_message = session.resend()

    return reply_message