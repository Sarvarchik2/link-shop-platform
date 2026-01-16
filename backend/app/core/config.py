from pydantic_settings import BaseSettings
import os

class Settings(BaseSettings):
    SECRET_KEY: str = "your-secret-key-here"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    # Priority: Env DATABASE_URL -> Env POSTGRES_URL -> Localhost
    DATABASE_URL: str = os.getenv("DATABASE_URL") or os.getenv("POSTGRES_URL") or "sqlite:///./database.db"
    UPLOAD_DIR: str = "uploads"
    BASE_URL: str = "http://localhost:8000"
    
    # Minio settings
    MINIO_ENDPOINT: str = os.getenv("MINIO_ENDPOINT", "localhost:9000")
    MINIO_ACCESS_KEY: str = os.getenv("MINIO_ACCESS_KEY", "minioadmin")
    MINIO_SECRET_KEY: str = os.getenv("MINIO_SECRET_KEY", "minioadmin")
    MINIO_BUCKET_NAME: str = os.getenv("MINIO_BUCKET_NAME", "media")
    MINIO_SECURE: bool = os.getenv("MINIO_SECURE", "False").lower() == "true"

    @property
    def SQLALCHEMY_DATABASE_URI(self) -> str:
        if self.DATABASE_URL.startswith("postgres://"):
             return self.DATABASE_URL.replace("postgres://", "postgresql://", 1)
        return self.DATABASE_URL
    
    # SMTP settings
    SMTP_HOST: str = os.getenv("SMTP_HOST", "smtp.gmail.com")
    SMTP_PORT: int = int(os.getenv("SMTP_PORT", 587))
    SMTP_USER: str = os.getenv("SMTP_USER", "sarvarikvarvarik@gmail.com")
    SMTP_PASSWORD: str = os.getenv("SMTP_PASSWORD", "lxxh dgbo fsfv wiyb")
    SMTP_FROM_EMAIL: str = os.getenv("SMTP_FROM_EMAIL", "sarvarikvarvarik@gmail.com")
    
    FRONTEND_URL: str = os.getenv("FRONTEND_URL", "http://localhost:3000")

    class Config:
        env_file = ".env"

settings = Settings()
