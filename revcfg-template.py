from EdgeGPT import ConversationStyle
# 选择使用的逆向库
# 目前支持以下库：
# - "acheong08/ChatGPT.V1": acheong08/ChatGPT库的V1版本
# - "acheong08/EdgeGPT": acheong08/EdgeGPT库，接入new bing
reverse_lib = "acheong08/ChatGPT.V1"

# [必填][❗此说明很重要，请您认真阅读❗] OpenAI账户信息
# 目前支持三种登录方式：账号密码登录、SessionToken登录、accessToken登录
# 1.适用于默认的注册方式得到的账号，2.适用于使用Google/Microsoft账号登录的账号，3.适用于中国大陆主机
# 以下默认使用账户密码方式登录。
#
# *若要使用SessionToken登录方式，请删掉email和password参数，添加session_token参数：
# 例如：
# openai_account = {
#   "session_token": "your session token"
# }
#
# *若要使用accessToken登录方式，请删掉email和password参数，添加access_token参数：
# 你可以在 https://chat.openai.com/api/auth/session 返回的数据中找到你的accessToken，记得先登录再获取
# 例如：
# openai_account = {
#   "access_token": "your access token"
# }
#
# 除了登录信息，还支持以下可选参数：
#  - proxy: 代理服务器地址，格式为"protocol:ip:port"，例如"https://localhost:1080"
#  - paid: 是否订阅了ChatGPT Plus服务，若为True则使用ChatGPT Plus服务
#  - model: 使用的模型, 若要使用GPT-4, 可以添加此参数并设置为"gpt-4"
# 可选参数填写格式示例:
# openai_account = [
#   {
#     "email": "your email",
#     "password": "your password",
#     "proxy": "https://localhost:1080",
#     "paid": True,
#     "model": "gpt-4"
#   }
# ]
#
# **若要使用多个账户均衡负载，可以以列表的形式添加多个账户信息，例如：
# openai_account = [
#   {
#     "email": "your email",
#     "password": "your password"
#   },
#   {
#     "email": "your email",
#     "password": "your password"
#   }
# ]
# 其中每个账户的格式符合前文所述的格式
openai_account = [
    {
        "email": "your email",  # 账户邮箱
        "password": "your password",  # 账户密码
    }
]

# 账号重新恢复使用的时间间隔
# 以分钟为单位
openai_account_resume_interval = 60

# New Bing的Style
# 请将此值设置为以下之一：
# ConversationStyle.creative     有创意
# ConversationStyle.balanced     平衡
# ConversationStyle.precise      精确
new_bing_style = ConversationStyle.balanced

# 使用New Bing时是否显示参考资料
output_references = True

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