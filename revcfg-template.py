from EdgeGPT.EdgeGPT import ConversationStyle
# 选择使用的逆向库
# 目前支持以下库：
# - "acheong08/ChatGPT.V1": acheong08/ChatGPT库的V1版本
# - "acheong08/EdgeGPT": acheong08/EdgeGPT库，接入new bing
# - "Soulter/hugging-chat-api": Soulter/hugging-chat-api库，接入hugging chat
# - "KoushikNavuluri/Claude-API": KoushikNavuluri/Claude-API库，接入Claude
# - "dsdanielpark/Bard-API": dsdanielpark/Bard-API库，接入Bard
# - "xtekky/gpt4free": xtekky/gpt4free库，接入多个平台的免费的 GPT-4，无需鉴权
reverse_lib = "acheong08/ChatGPT.V1"

# [必填][❗此说明很重要，请您认真阅读❗] OpenAI账户信息
# *仅使用acheong08/ChatGPT.V1时填写
# 目前支持三种登录方式：
# - 账号密码登录(仅支持ChatGPT Plus账号)
# - SessionToken登录(仅Microsoft、Google账号注册的账号)
# - accessToken登录(普通账号请使用此方法登录)
#
# *账号密码登录方式，例如：
# openai_account = {
#   "email": "your email",
#   "password": "your password"
# }
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
#     "access_token": "your access_token",
#     "proxy": "https://localhost:1080",
#     "paid": True,
#     "model": "gpt-4"
#   }
# ]
#
# **若要使用多个账户均衡负载，可以以列表的形式添加多个账户信息，例如：
# openai_account = [
#   {
#     "access_token": "your access_token",
#   },
#   {
#     "access_token": "your access_token",
#   }
# ]
# 其中每个账户的格式符合前文所述的格式
openai_account = [
    {
        "access_token": "your access_token",
    }
]

# 账号重新恢复使用的时间间隔
# 以分钟为单位
openai_account_resume_interval = 60

# New Bing的代理地址
# 参考config.py中openai的代理地址
# 若为None则不使用代理
new_bing_proxy = None

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

# 使用 gpt4free 时，仅使用的适配器名称列表
# 程序将在这些适配器中选择一个可用的适配器
# 例如：
# g4f_use_adapters = ['Acytoo', 'FakeGpt']
# 
# 若为 空列表 则会测试所有适配器并自动选择
# 所有适配器列表可以在
# https://github.com/xtekky/gpt4free/blob/main/g4f/Provider/__init__.py
# 中找到
# 也可以再启动机器人之后，发送命令 !provider 列出所有适配器
#
# 注意：设置此字段可能会影响可用性，请确认指定的适配器可用
g4f_use_adapters = []

# 使用 gpt4free 时，排除的适配器名称
# 此字段优先级高于 g4f_use_adapters
g4f_exclude_adapters = []
