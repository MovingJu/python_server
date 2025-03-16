import os
import dotenv
from bcrypt import hashpw, checkpw

from config import key_env

# 환경 변수 파일 로드
SALT_FILE = key_env
dotenv.load_dotenv(SALT_FILE)

SALT = os.getenv("BCRYPT_SALT")

SALT = SALT.encode()

def encryption(user_pw: str) -> bytes:
    """저장된 salt를 사용하여 비밀번호 해싱"""
    return hashpw(user_pw.encode(), SALT)


def verify_password(user_pw: str, stored_hash: bytes) -> bool:
    """입력된 비밀번호가 저장된 해시와 일치하는지 검증"""
    return encryption(user_pw) == stored_hash


if __name__ == "__main__":
    hashed = encryption("my_secure_password")
    print("🔒 Hashed Password:", hashed)

    # 검증
    print("✅ Password Match:", verify_password("my_secure_password", hashed))
    print("❌ Wrong Password Match:", verify_password("wrong_password", hashed))