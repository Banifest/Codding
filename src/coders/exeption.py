from typing import Optional


class DecodingException(Exception):
    message = ""
    status: int

    def __init__(self, message: str, status: Optional[int]):
        self.message = message
        if status is not None: self.status = status
