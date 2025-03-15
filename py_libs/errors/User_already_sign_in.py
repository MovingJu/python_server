"""Raise User_already_sign_in error when user_id and user_pw are in users.csv"""

class User_already_sign_in(Exception):
    def __init__(self, message):
        self.message = message
        super().__init__(self.message)