class DecodingException(Exception):
    message = ""
    result = ""

    def __init__(self, message: str):
        self.message = message