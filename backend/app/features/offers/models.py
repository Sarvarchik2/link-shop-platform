from sqlalchemy import Column, Integer, String, Float, Boolean, DateTime
from datetime import datetime
from app.db.base_class import Base

class Offer(Base):
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    title_ru = Column(String, nullable=True)
    title_en = Column(String, nullable=True)
    title_uz = Column(String, nullable=True)
    
    description = Column(String, nullable=False)
    description_ru = Column(String, nullable=True)
    description_en = Column(String, nullable=True)
    description_uz = Column(String, nullable=True)
    
    price = Column(Float, nullable=True)
    price_text = Column(String, nullable=True)
    price_text_ru = Column(String, nullable=True)
    price_text_en = Column(String, nullable=True)
    price_text_uz = Column(String, nullable=True)
    
    contact_text = Column(String, default="Свяжитесь с нами для покупки")
    contact_text_ru = Column(String, nullable=True)
    contact_text_en = Column(String, nullable=True)
    contact_text_uz = Column(String, nullable=True)
    
    contact_email = Column(String, nullable=True)
    contact_phone = Column(String, nullable=True)
    is_active = Column(Boolean, default=True)
    display_order = Column(Integer, default=0)
    created_at = Column(DateTime, default=datetime.utcnow)
