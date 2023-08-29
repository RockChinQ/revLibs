from typing import Tuple


class RevLibInterface:
    """逆向库接口"""

    @staticmethod
    def create_instance() -> tuple["RevLibInterface", bool, dict]:
        raise NotImplementedError

    def get_rev_lib_inst(self):
        raise NotImplementedError

    def get_reply(self, prompt: str, **kwargs) -> Tuple[str, dict]:
        raise NotImplementedError

    def reset_chat(self, **kwargs):
        raise NotImplementedError

    def rollback(self):
        raise NotImplementedError
