import time
import plugins.revLibs.pkg.process.revss as revss
from pkg.plugin.host import PluginHost
import logging
from mirai import MessageChain
from mirai.models.message import ForwardMessageNode
from plugins.revLibs.pkg.models.forward import Forward, ForwardMessageDiaplay
import traceback

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
            # 使用迭代器
            if revcfg.blog_msg_strategy == "send_section":
                section_count = 0
                for section in session.get_reply(prompt):
                    section_count += 1
                    logging.info("分节回复: {}".format(section[:min(50, len(section))]))
                    if kwargs['launcher_type'] == 'group':
                        host.send_group_message(kwargs['launcher_id'], "{}".format(revcfg.reply_prefix) + section)
                    elif kwargs['launcher_type'] == 'person':
                        host.send_person_message(kwargs['launcher_id'], "{}".format(revcfg.reply_prefix) + section)

                if section_count > 1:
                    reply_message = "<已发送完毕>"
            elif revcfg.blog_msg_strategy == "forward_msg_component":
                all_reply = ""

                use_forward_msg_component = False
                for section in session.get_reply(prompt):
                    if all_reply != "":
                        use_forward_msg_component = True
                    all_reply += section

                if use_forward_msg_component:
                    import config

                    bot_uin = config.mirai_http_api_config['qq']

                    forward_msg_node = ForwardMessageNode(
                        sender_id=bot_uin,
                        sender_name="revLibs",
                        message_chain=MessageChain([all_reply])
                    )

                    forward_msg_display = ForwardMessageDiaplay(
                        title="群聊的聊天记录",
                        brief="[聊天记录]",
                        source="聊天记录",
                        preview=[all_reply],
                        summary="查看1条转发消息"
                    )

                    message_chain = Forward(
                        display=forward_msg_display,
                        node_list=[forward_msg_node]
                    )

                    logging.info("[rev] 回复{}消息：{}".format(session_name, all_reply[:min(50, len(all_reply))]))

                    if kwargs['launcher_type'] == 'group':
                        host.send_group_message(kwargs['launcher_id'], message_chain)
                    elif kwargs['launcher_type'] == 'person':
                        host.send_person_message(kwargs['launcher_id'], message_chain)
                else:
                    # logging.info("[rev] 回复{}消息：{}".format(session_name, all_reply[:min(50, len(all_reply))]))
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
