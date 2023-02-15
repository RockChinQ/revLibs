# RevLib Support for QChatGPT

得益于[QChatGPT项目](https://github.com/RockChinQ/QChatGPT)的插件功能，此插件将允许接入ChatGPT网页版用以替换原项目主线的GPT-3模型接口，提升回复质量。

## 使用方式

> 若您未安装QChatGPT程序，请先查看原仓库[文档](https://github.com/RockChinQ/QChatGPT)

使用管理员账号私聊机器人发送指令:

```
!plugin https://github.com/RockChinQ/revLibs
```

等待程序获取源码，并解决依赖，这可能需要数分钟的时间。  
安装完毕后，请发送:
```
!reload
```
重载插件，生成配置文件。  
之后到`QChatGPT`程序目录编辑`revcfg.py`文件，根据注释修改必填配置项
