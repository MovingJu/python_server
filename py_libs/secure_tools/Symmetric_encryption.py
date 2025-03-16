from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
import base64
import os
import dotenv

from config import key_env

dotenv.load_dotenv(key_env)

class Symmetric_Encryption:
    def __init__(self, key: bytes = None):
        """AES 256-bit (32-byte) 키 생성 또는 사용"""
        
        self.key = key

    def encrypt(self, plaintext: str) -> str:
        """텍스트 암호화"""
        cipher = AES.new(self.key, AES.MODE_CBC, iv := os.urandom(16))  # CBC 모드 사용
        ciphertext = cipher.encrypt(pad(plaintext.encode(), AES.block_size))
        return base64.b64encode(iv + ciphertext).decode()  # IV + 암호문을 Base64 인코딩 후 반환

    def decrypt(self, encrypted_text: str) -> str:
        """암호문 복호화"""
        raw_data = base64.b64decode(encrypted_text)  # Base64 디코딩
        iv, ciphertext = raw_data[:16], raw_data[16:]  # IV와 암호문 분리
        cipher = AES.new(self.key, AES.MODE_CBC, iv)
        return unpad(cipher.decrypt(ciphertext), AES.block_size).decode()

if __name__ == "__main__":
    dotenv.load_dotenv(key_env)
    crypto = Symmetric_Encryption(bytes.fromhex(os.getenv('AUTHORITY_KEY')))
    print("🔑 사용된 키:", crypto.key.hex())
    
    test = ['1', '2', '3', '5']

    encrypted = [crypto.encrypt(i) for i in test]  # 암호화
    test = [crypto.encrypt(i) for i in test]
    decrypted = [crypto.decrypt(i) for i in test]  # 복호화

    print("🔒 암호화된 텍스트:", encrypted)
    print("🔓 복호화된 텍스트:", decrypted)
