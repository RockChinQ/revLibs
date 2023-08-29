# RevLib Support for QChatGPT

> 2023/8/14 现已支持`Claude`和`Bard`，请查看下方的使用方法  
> 2023/8/03 逆向库现已支持`函数调用`, 配置方法同[主程序配置方法](https://github.com/RockChinQ/QChatGPT/wiki/%E6%8F%92%E4%BB%B6%E4%BD%BF%E7%94%A8-%E5%86%85%E5%AE%B9%E5%87%BD%E6%95%B0)  
> 2023/5/14 已支持通过[Soulter/hugging-chat-api](https://github.com/Soulter/hugging-chat-api)接入[HuggingChat](https://huggingface.co/chat/)  


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

## Cookies获取方法

大部分逆向库基于Cookies登录，因此需要获取Cookies。这里讲解了获取一个网站的Cookies的详细步骤，您可以先查看下方选择逆向库的步骤，到需要的网站使用以下方式获取Cookies。

1. 安装适用于[Chrome/Edge](https://chrome.google.com/webstore/detail/cookie-editor/hlkenndednhfkekhgcdicdfddnkalmdm) 或 [Firefox](https://addons.mozilla.org/en-US/firefox/addon/cookie-editor/) 的Cookies编辑器插件
2. 访问 目标网站
3. 打开这个插件
4. 点击 `Export` 按钮, 复制JSON格式的Cookies
5. 将`Cookies`保存到指定的文件中

## 选择逆向库

目前支持的逆向库及使用方式如下, 下方所述文件保存位置均为主程序`config.py`同目录，若无此文件，请自行创建：

<details>
<summary>ChatGPT网页版</summary>

本插件默认使用的逆向库，使用方法请参考配置文件注释。
使用的是 [acheong08/ChatGPT](https://github.com/acheong08/ChatGPT)  
</details>

<details>
<summary>New Bing(暂不可用)</summary>

使用的是 [acheong08/EdgeGPT](https://github.com/acheong08/EdgeGPT)  

 - 修改`revcfg.py`中的`reverse_lib`的值为`acheong08/EdgeGPT`
 - 获取[NewBing](https://bing.com/chat)的Cookies，保存到`cookies.json`中

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
2. 获取[HuggingChat](https://huggingface.co/chat/)的Cookies，保存到`hugchat.json`中

</details>

<details>
<summary>Claude</summary>

1. 在`revcfg.py`中修改`reverse_lib`的值为`KoushikNavuluri/Claude-API`
2. 获取[Claude](https://claude.ai/chats)的Cookies，保存到`claude.json`中

</details>

<details>

<summary>Google Bard</summary>

1. 在`revcfg.py`中修改`reverse_lib`的值为`dsdanielpark/Bard-API`
2. 获取[Bard](https://bard.google.com/)的Cookies，保存到`bard.json`中

</details>

<details>
<summary>gpt4free</summary>

接入[xtekky/gpt4free](https://github.com/xtekky/gpt4free)自动从数个平台选择可用的 GPT-4，**无需鉴权**，但很不稳定，仅需要在`revcfg.py`中修改`reverse_lib`的值为`xtekky/gpt4free`即可。

</details>

<br/>

### 🚫请勿修改`revcfg-template.py`的内容，配置项请在主程序`config.py`同目录的`revcfg.py`中修改🚫

## 特别感谢

> 向所有致力于人工智能民主化的开发者致敬。  
> Salute to all developers committed to the democratization of artificial intelligence.  
> 인공지능 민주화에 힘쓴 모든 개발자들에게 경의를 표합니다.  
> 人工知能の民主化に取り組むすべての開発者に敬意を表します。
