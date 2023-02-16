from typing import Tuple


class RevLibInterface:
    def get_reply(prompt: str, **kwargs) -> Tuple[str, dict]:
        raise NotImplementedError