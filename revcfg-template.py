# OpenAI账户信息
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