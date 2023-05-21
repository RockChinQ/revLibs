# RevLib Support for QChatGPT

> 2023/5/14 已支持通过[Soulter/hugging-chat-api](https://github.com/Soulter/hugging-chat-api)接入[HuggingChat](https://huggingface.co/chat/)  
> 2023/5/1  不再向New Bing发送情景预设，以防止被拒绝回复。  
> 2023/3/15 现已支持New Bing，请查看下方使用方法。  
> 2023/3/15 OpenAI已开放使用GPT-4模型的ChatGPT，目前仅支持ChatGPT Plus账户使用，请使用`!plugin update`更新插件，查看`revcfg-template.py`的账户配置说明并修改`revcfg.py`文件。  


得益于[QChatGPT项目](https://github.com/RockChinQ/QChatGPT)的插件功能，此插件将允许接入`ChatGPT网页版`用以替换原项目主线的GPT-3模型接口，提升回复质量。  
[官方接口与ChatGPT网页版的区别？](https://github.com/RockChinQ/QChatGPT/wiki/%E5%AE%98%E6%96%B9%E6%8E%A5%E5%8F%A3%E4%B8%8EChatGPT%E7%BD%91%E9%A1%B5%E7%89%88)

## 安装方式

> 若您未安装QChatGPT程序，请先查看原仓库[文档](https://github.com/RockChinQ/QChatGPT)  
> 目前已支持中国主机使用，请在revcfg.py中修改openai_account字段，按照注释使用access_token方式登录

使用管理员账号私聊机器人发送指令:

```
!plugin https://github.com/RockChinQ/revLibs
```

若无法访问GitHub，可以使用Gitee镜像

```
!plugin https://gitee.com/RockChin/revLibs
```

等待程序获取源码，并解决依赖，这可能需要数分钟的时间。  
安装完毕后，请发送:
```
!reload
```
重载插件，生成配置文件，**关闭主程序**。  
到`QChatGPT`程序目录编辑`revcfg.py`文件，根据注释修改必填配置项。  
配置完成后重新启动主程序以使用。

## 选择逆向库

目前支持的逆向库及使用方式如下:

<details>
<summary>ChatGPT网页版</summary>

本插件默认使用的逆向库，使用方法请参考上方文档及配置文件注释。  
使用的是 [acheong08/ChatGPT](https://github.com/acheong08/ChatGPT)  
</details>

<details>
<summary>New Bing</summary>

使用的是 [acheong08/EdgeGPT](https://github.com/acheong08/EdgeGPT)  

 - 修改`revcfg.py`中的`reverse_lib`的值为`acheong08/EdgeGPT`即可，不需要鉴权

#### 配置

- new bing逆向库默认输出参考资料, 若不需要, 请在`revcfg.py`中设置:

```python
output_references = False
```

- 设置New Bing的风格

查看revcfg.py中的`new_bing_style`字段，按照说明更改。在运行期间可以通过指令`!style <风格（创意、平衡、精确）>`来更改风格。

</details>

<details>
<summary>HuggingChat</summary>

1. 在`revcfg.py`中修改`reverse_lib`的值为`Soulter/hugging-chat-api`
2. 安装适用于[Chrome/Edge](https://chrome.google.com/webstore/detail/cookie-editor/hlkenndednhfkekhgcdicdfddnkalmdm) 或 [Firefox](https://addons.mozilla.org/en-US/firefox/addon/cookie-editor/) 的Cookies编辑器插件
3. 访问 `huggingface.co/chat`
4. 打开这个插件
5. 点击 `Export` 按钮, 复制JSON格式的Cookies
6. 在QChatGPT主程序`main.py`同目录下新建文件`hugchat.json`, 将刚才复制的内容粘贴进去

</details>
<br/>

### 🚫请勿修改`revcfg-template.py`的内容，配置项请在主程序`config.py`同目录的`revcfg.py`中修改🚫