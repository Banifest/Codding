class DecodingException(Exception):
    message = ""
    result = ""

    def __init__(self, message: str):
        self.message = message

    def __init__(self, message, status):
        self.message = message
        self.result = status
