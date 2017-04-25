class DecodingException(Exception):
    message = ""
    result = ""

    def __init__(self, message):
        self.message = message
