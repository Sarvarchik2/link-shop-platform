from sqlalchemy import Column, Integer, String, DateTime, Boolean
from datetime import datetime
from app.db.base_class import Base

class User(Base):
    id = Column(Integer, primary_key=True, index=True)
    phone = Column(String, unique=True, index=True, nullable=False)
    email = Column(String, unique=True, index=True, nullable=True)
    password_hash = Column(String, nullable=False)
    first_name = Column(String, default="")
    last_name = Column(String, default="")
    role = Column(String, default="user") # user, shop_owner, platform_admin
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Email verification
    is_email_verified = Column(Boolean, default=False)
    email_verification_code = Column(String, nullable=True)
    verification_expires_at = Column(DateTime, nullable=True)
    
    # Password reset
    reset_password_token = Column(String, nullable=True)
    reset_password_expires_at = Column(DateTime, nullable=True)
