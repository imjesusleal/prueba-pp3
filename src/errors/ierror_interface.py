from abc import ABC

class IError(Exception, ABC):
    def __init__(self,msg: str, code: int):
        super().__init__(msg)
        self.msg = msg
        self.http_code = code