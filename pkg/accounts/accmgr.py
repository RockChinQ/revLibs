import time


def get_account_list():
    import revcfg
    if type(revcfg.openai_account) is dict:
        revcfg.openai_account = [revcfg.openai_account]
    return revcfg.openai_account


def get_account_brief_name(account: dict):
    if 'email' in account:
        return account['email']
    elif 'session_token' in account:
        return "sessionToken: "+account['session_token'][:8]
    elif 'access_token' in account:
        return "accessToken: "+account['access_token'][:8]
    else:
        return "未知账户"


def move_account_to_end(account: dict):
    # 将账户移动到末尾
    import revcfg

    account_list = get_account_list()
    account_list.remove(account)
    account_list.append(account)
    revcfg.openai_account = account_list


def delete_invalid_attr(account: dict):
    temp_dict = dict(account)
    if 'invalid_at' in temp_dict:
        del temp_dict['invalid_at']
    return temp_dict


def use_account() -> tuple[bool, dict]:
    # 计算并返回下一个账户
    import revcfg

    account_resume_interval = revcfg.openai_account_resume_interval if hasattr(revcfg, 'openai_account_resume_interval') else 60
    
    now = int(time.time())
    for account in get_account_list():
        if 'invalid_at' in account:
            if account['invalid_at'] < now - account_resume_interval * 60:
                move_account_to_end(account)
                return True, delete_invalid_attr(account)

        if 'invalid_at' not in account:
            move_account_to_end(account)
            return True, delete_invalid_attr(account)
    
    move_account_to_end(get_account_list()[0])
    return False, delete_invalid_attr(get_account_list()[0])
    

def report_invalidation(account: dict):
    # 报告账户失效

    for acc in get_account_list():
        if 'email' in acc and 'email' in account and acc['email'] == account['email']:
            acc['invalid_at'] = int(time.time())
            return
        elif 'session_token' in acc and 'session_token' in account and acc['session_token'] == account['session_token']:
            acc['invalid_at'] = int(time.time())
            return
        elif 'access_token' in acc and 'access_token' in account and acc['access_token'] == account['access_token']:
            acc['invalid_at'] = int(time.time())
            return
    
    


