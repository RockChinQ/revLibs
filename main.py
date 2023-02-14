from pkg.plugin.models import *
from pkg.plugin.host import EventContext, PluginHost

"""
接入ChatGPT的逆向库
"""


# 注册插件
@register(name="revLibs", description="接入acheong08/ChatGPT等逆向库", version="0.1", author="RockChinQ")
class HelloPlugin(Plugin):

    # 插件加载时触发
    # plugin_host (pkg.plugin.host.PluginHost) 提供了与主程序交互的一些方法，详细请查看其源码
    def __init__(self, plugin_host: PluginHost):
        pass

    # 当收到个人消息时触发
    @on(PersonNormalMessageReceived)
    def person_normal_message_received(self, event: EventContext, **kwargs):
        pass

    # 当收到群消息时触发
    @on(GroupNormalMessageReceived)
    def group_normal_message_received(self, event: EventContext, **kwargs):
        pass

    # 插件卸载时触发
    def __del__(self):
        pass
