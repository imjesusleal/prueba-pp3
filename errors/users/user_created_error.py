from errors.ierror_interface import IError


class UserCreatedError(IError):
    def __init__(self, msg: str):
        super().__init__(msg)
        self.msg = msg