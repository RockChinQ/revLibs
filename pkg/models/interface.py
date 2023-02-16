from typing import Tuple


class RevLibInterface:
    """逆向库接口"""

    def get_rev_lib_inst():
        raise NotImplementedError

    def get_reply(prompt: str, **kwargs) -> Tuple[str, dict]:
        raise NotImplementedError

    def reset_chat():
        raise NotImplementedError

    def rollback():
        raise NotImplementedError
