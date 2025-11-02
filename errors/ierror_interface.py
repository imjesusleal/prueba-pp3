from abc import ABC

class IError(Exception, ABC):
    def __init__(self,msg, code):
        super().__init__(msg, code)
        self.msg = msg
        self.http_code = code