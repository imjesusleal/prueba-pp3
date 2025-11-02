from errors.ierror_interface import IError


class RefreshTokenCreatedError(IError):
    def __init__(self, msg: str):
        super().__init__(msg)
        self.msg = msg