# 使用acheong08/ChatGPT库的方式
# 目前仅支持V1版本
acheong_chatgpt_version = "V1"

# [必填] OpenAI账户信息
# 目前支持两种登录方式：账号密码登录 和 SessionToken登录
# 前者适用于默认的注册方式得到的账号，后者适用于使用Google/Microsoft账号登录的账号
# 以下默认的参数为账号密码登录方式，若使用SessionToken登录方式，请删掉email和password参数，添加session_token参数
# 
# 除了登录信息，还支持以下可选参数：
#  - proxy: 代理服务器地址，格式为"protocol:ip:port"，例如"https://localhost:1080"
#  - paid: 是否订阅了ChatGPT Plus服务，若为True则使用ChatGPT Plus服务
openai_account = {
    "email": "your email",  # 账户邮箱
    "password": "your password",  # 账户密码
}

# 消息回复前缀
# 建议保留此前缀，以便区分GPT-3和此插件的回复
reply_prefix = "[REV]"

# 获取回复失败时的重试次数
# 若为0则不重试
retry_when_fail = 3

# 超长消息阈值
# 若消息长度超过此阈值，则按照以下策略处理
# 如果你不需要使用分节功能（即任何消息都以普通消息的形式回复），
# 请将此值设置为超大的值（如 2147483647）
blog_msg_threshold = 256

# 超长消息处理策略
# - "send_section": 发送前部分消息，继续等待回复
# - "forward_msg_component": 以转发消息的形式发送
blog_msg_strategy = "forward_msg_component"