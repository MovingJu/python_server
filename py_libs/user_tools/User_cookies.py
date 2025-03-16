import pandas as pd
import dotenv
import os

from py_libs import errors, secure_tools
from main import users_csv, key_env

class User_cookies:
    """Management tools for user sign_in, handling user informations like object.
    You need to use try-except syntax at least once."""

    def __new__(cls, user_id:str, user_pw:str, *args, **kwargs):
        
        users = pd.read_csv(users_csv)
        if user_id in users['user_id'].values:
            raise errors.User_already_sign_in("Use different username.")
        
        if errors.detect_sql_injection(user_id) or errors.detect_sql_injection(user_pw):
            kwargs['sql_tries'] = kwargs.get('sql_tries', 0) + 1
            raise errors.Sql_injection_detected(kwargs['sql_tries'])
            
        
        return super().__new__(cls)
    
    def __init__(self, user_id:str, user_pw:str, authorities:set[str]=set()):
        try: 
            self.user_id = user_id
            self.user_pw = secure_tools.encryption(user_pw)
            self.authorities = authorities
            self.authorities.update({"readable"})

            dotenv.load_dotenv(key_env)
            crypto = secure_tools.Symmetric_Encryption(bytes.fromhex(os.getenv('AUTHORITY_KEY')))
            self.authorities = {crypto.encrypt(i) for i in self.authorities}

        
            self.cookies: dict[str:str, str:str, str:set] = {"user_id":self.user_id, "user_pw":self.user_pw, "authorities":str(self.authorities)}
        
        except Exception:
            raise errors.Login_fail_error("Something went wrong while sign_in.")
        
        except errors.Login_fail_error as e:
            return e

    def get_cookies(self):
        return self.cookies