def encryption(user_pw: str) -> bytes:
    """function that hashes user password"""

    from bcrypt import gensalt, hashpw
    salt = gensalt()
    hashed_pw = hashpw(user_pw.encode(), salt)
    
    return hashed_pw