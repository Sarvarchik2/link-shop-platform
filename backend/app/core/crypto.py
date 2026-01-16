from cryptography.fernet import Fernet
from app.core.config import settings

class Crypto:
    def __init__(self):
        self.fernet = Fernet(settings.TELEGRAM_ENCRYPTION_KEY.encode())

    def encrypt(self, data: str) -> str:
        if not data:
            return None
        return self.fernet.encrypt(data.encode()).decode()

    def decrypt(self, encrypted_data: str) -> str:
        if not encrypted_data:
            return None
        try:
            return self.fernet.decrypt(encrypted_data.encode()).decode()
        except:
            return None

crypto = Crypto()
