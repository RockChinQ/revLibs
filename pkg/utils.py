from pip._internal import main as pipmain

def upgrade_revlibs():
    """更新逆向库"""
    pipmain(['install', '--upgrade', 'revChatGPT', '--quiet'])
    import main
    main.reset_logging()