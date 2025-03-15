"""Raise Login_fail_error if something went wrong while trying to login."""

class Login_fail_error(Exception):
    def __init__(self, message="Fail to login."):
        self.message = message
        super().__init__(self.message)

