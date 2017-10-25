class CodingException(Exception):
    message = ""
    status: int

    def __init__(self, message: str, status=None):
        self.message = message
        if status is not None: self.status = status

