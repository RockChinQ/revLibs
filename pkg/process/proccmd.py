import plugins.revLibs.pkg.process.revss as revss

def process_command(session_name: str, **kwargs) -> str:
    """处理命令"""

    cmd = kwargs['command']
    params = kwargs['params']

    reply_message = ""

    if cmd == 'reset':
        session: revss.RevSession = revss.get_session(session_name)
        if len(params) >= 1:
            prompt_whole_name = session.reset(params[0])
            reply_message = "已重置会话，使用情景预设: {}".format(prompt_whole_name)
        else:
            session.reset()
            reply_message = "已重置会话"
    elif cmd == 'list':
        session: revss.RevSession = revss.get_session(session_name)
        page = 1
        if len(params)>=1:
            page = int(params[0])
        
        cbinst = session.get_rev_lib_inst()
        from revChatGPT.V1 import Chatbot
        assert isinstance(cbinst, Chatbot)

        conversations = cbinst.get_conversations((page-1)*10, 10)

        reply_message = "会话列表 (第{}页) 本页{}个会话:\n".format(page, len(conversations))
        for conversation in conversations:
            reply_message += "#{}: {}\n".format(conversation['id'], conversation['create_time'])

    elif cmd == 'prompt':
        # cbinst = session.get_rev_lib_inst()
        # from revChatGPT.V1 import Chatbot
        # assert isinstance(cbinst, Chatbot)
        # reply_message = str(cbinst.get_msg_history(session.conversation_id))
        reply_message = "正在使用逆向库，暂不支持查看历史消息"
    elif cmd == "last":
        reply_message = "正在使用逆向库，暂不支持切换到前一次会话"
    elif cmd == "next":
        reply_message = "正在使用逆向库，暂不支持切换到后一次会话"
    elif cmd == "resend":
        session: revss.RevSession = revss.get_session(session_name)
        if session.__ls_prompt__ == "":
            reply_message = "没有上一条成功回复的消息"
        else:
            reply_message = session.resend()
    elif cmd == "accs":
        """查看每个账户的使用情况"""
        import plugins.revLibs.pkg.accounts.accmgr as accmgr

        reply_message = "账户列表:\n"

        for account in accmgr.get_account_list():
            """
                - 账户名称
            """
            reply_message += "账户: {}\n  - ".format(accmgr.get_account_brief_name(account))

            using = False
            for k in revss.__sessions__:
                v: revss.RevSession = revss.__sessions__[k]
                if accmgr.get_account_brief_name(v.using_account) == accmgr.get_account_brief_name(account):
                    reply_message += v.name + ", "
                    using = True
            if not using:
                reply_message += "未使用"
            else:
                reply_message = reply_message[:-2]

            reply_message += "\n\n"

    return reply_message[:-1]
