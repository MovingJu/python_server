"""Management tools for user sign_in, handling user informations like object."""

from py_libs import errors, secure_tools

class User_cookies:

    def __new__(cls, user_id:str, user_pw:str, *args, **kwargs):
        if errors.detect_sql_injection(user_id) or errors.detect_sql_injection(user_pw):
            kwargs['sql_tries'] = kwargs.get('sql_tries', 0) + 1
            raise errors.Sql_injection_detected(kwargs['sql_tries'])
        return super().__new__(cls) 
    
    def __init__(self, user_id:str, user_pw:str, authorities:set=set(), **kwargs: dict[str:"Int, String, etc.."]):
        try: 
            self.user_id = user_id
            self.user_pw = secure_tools.encryption(user_pw)
            self.kwargs = kwargs
            self.authorities = authorities.update({"readable"})
        
            self.cookies: dict[str:] = {"user_id":self.user_id, "user_pw":self.user_pw, "authorities":self.authorities}
        
        except Exception:
            raise errors.Login_fail_error("Something went wrong while sign_in.")
        
        except errors.Login_fail_error as e:
            return e
