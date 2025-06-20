# UnexceptedResponse
class UnexceptedResponse(Exception):
    def __init__(self, response):
        message=f"Unexcepted response: {response}"
        super().__init__(message) 