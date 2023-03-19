import time
import plugins.revLibs.pkg.process.revss as revss
from pkg.plugin.host import PluginHost
import logging
from mirai import MessageChain
from mirai.models.message import ForwardMessageNode
from plugins.revLibs.pkg.models.forward import Forward, ForwardMessageDiaplay
import traceback
import pkg.utils.context as context
import pkg.qqbot.manager as qqmgr

__host__: PluginHost = None


def process_message(session_name: str, prompt: str, host: PluginHost, **kwargs) -> str:
    """处理消息"""
    global __host__

    logging.info("[rev] 收到{}消息: {}".format(session_name, prompt))

    if __host__ is None:
        __host__ = host
    if host is None:
        host = __host__

    import revcfg

    # 重试循环
    fail_times = 0
    reply_message = ""
    while True:
        session: revss.RevSession = revss.get_session(session_name)
        try:
            if hasattr(revcfg, "blog_msg_strategy"):
                logging.warning("[rev] 逆向库不再进行长消息处理，请使用主程序的长消息处理功能，详情请查看主程序的config-template.py")
            
            all_reply = ""

            for section in session.get_reply(prompt):
                all_reply += section

            reply_message = all_reply

            break
        except Exception as e:
            traceback.print_exc()
            if str(e).__contains__("Too many requests in 1 hour"):
                session.__init__(session_name)
                logging.warn("超过一小时限次，切换会话账户")
                continue

            if fail_times < revcfg.retry_when_fail:
                fail_times += 1
                logging.warn("失败，重试({}/{})...".format(fail_times, revcfg.retry_when_fail))
                time.sleep(2)
                continue
            else:
                raise e

    return reply_message
