"""Raise Sql_injection_detected if sql injection is detected."""

class Sql_injection_detected(Exception):
    
    def __init__(self, sql_tries:int):
        self.sql_tries = sql_tries
        if self.sql_tries <= 1:
            super().__init__("You can't use special characters.")
        else:
            self.log_error()
            super().__init__("NEVERMIND WHILE I'M BREATHING")

    def log_error(self):
        print(f"**NOTICE: {self} tried to do SQL injection for {self.sql_tries} times.**")