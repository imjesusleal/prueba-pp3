from abc import ABC

class IError(Exception, ABC):
    def __init__(self,msg):
        super().__init__(msg)
        self.msg = msg