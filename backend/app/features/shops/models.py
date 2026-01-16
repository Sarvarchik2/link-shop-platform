from sqlalchemy import Column, Integer, String, DateTime, Boolean, ForeignKey, JSON
from datetime import datetime
from app.db.base_class import Base

class Shop(Base):
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    slug = Column(String, unique=True, index=True, nullable=False)
    owner_id = Column(Integer, ForeignKey("user.id"), nullable=False)
    description = Column(String, nullable=True)
    logo_url = Column(String, nullable=True)
    subscription_status = Column(String, default="trial")
    subscription_expires_at = Column(DateTime, nullable=True)
    subscription_plan_id = Column(Integer, ForeignKey("subscriptionplan.id"), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    is_active = Column(Boolean, default=True)
    # Contact information
    email = Column(String, nullable=True)
    phone = Column(String, nullable=True)
    address = Column(String, nullable=True)
    # Social media links
    telegram = Column(String, nullable=True)
    instagram = Column(String, nullable=True)
    facebook = Column(String, nullable=True)
    twitter = Column(String, nullable=True)
    whatsapp = Column(String, nullable=True)
    
    # Telegram Bot Integration
    telegram_bot_token = Column(String, nullable=True)
    is_bot_active = Column(Boolean, default=False)
    
    # Delivery Settings
    # { "type": "free" | "fixed" | "regional", "price": 0, "regions": { "Toshkent": 10000 } }
    delivery_settings = Column(JSON, nullable=True, default={})

class UserStoreTelegram(Base):
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("user.id"), nullable=False)
    store_id = Column(Integer, ForeignKey("shop.id"), nullable=False)
    telegram_chat_id = Column(String, nullable=False) # Storely uses BigInt, but String is safer for all IDs
    
    # Ensure a user can only have one chat_id per shop
    __table_args__ = (
        # UniqueConstraint('user_id', 'store_id', name='inx_user_store_telegram'),
    )

