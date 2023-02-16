import plugins.revLibs.pkg.process.revss as revss

def process_message(session_name: str, prompt: str, **kwargs) -> str:
    """处理消息"""
    session: revss.RevSession = revss.get_session(session_name)

    reply_message = session.get_reply(prompt, **kwargs)

    return reply_message