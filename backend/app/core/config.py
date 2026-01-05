from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    SECRET_KEY: str = "your-secret-key-here"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    DATABASE_URL: str = os.getenv("DATABASE_URL", "postgresql://localhost/linkshop")
    UPLOAD_DIR: str = "uploads"
    BASE_URL: str = "http://localhost:8000"

    @property
    def SQLALCHEMY_DATABASE_URI(self) -> str:
        if self.DATABASE_URL.startswith("postgres://"):
             return self.DATABASE_URL.replace("postgres://", "postgresql://", 1)
        return self.DATABASE_URL

    class Config:
        env_file = ".env"

settings = Settings()
