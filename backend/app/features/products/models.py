from sqlalchemy import Column, Integer, String, Float, Boolean, ForeignKey, DateTime
from app.db.base_class import Base
from datetime import datetime

class Product(Base):
    id = Column(Integer, primary_key=True, index=True)
    
    # Multilingual fields
    name_uz = Column(String, nullable=False)
    name_ru = Column(String, nullable=False)
    name_en = Column(String, nullable=False)
    
    description_uz = Column(String, nullable=False)
    description_ru = Column(String, nullable=False)
    description_en = Column(String, nullable=False)
    
    price = Column(Float, nullable=False)
    discount = Column(Float, default=0.0)
    image_url = Column(String, nullable=False)
    images = Column(String, nullable=True)  # JSON string
    
    # Multilingual category and brand
    category_uz = Column(String, nullable=False)
    category_ru = Column(String, nullable=False)
    category_en = Column(String, nullable=False)
    
    brand_uz = Column(String, nullable=False)
    brand_ru = Column(String, nullable=False)
    brand_en = Column(String, nullable=False)
    
    rating = Column(Float, default=0.0)
    reviews_count = Column(Integer, default=0)
    is_favorite = Column(Boolean, default=False)
    stock = Column(Integer, default=0)
    sizes = Column(String, nullable=True)    # JSON string (legacy)
    colors = Column(String, nullable=True)   # JSON string (legacy)
    variants = Column(String, nullable=True) # JSON string
    shop_id = Column(Integer, ForeignKey("shop.id"), nullable=True)
    is_preorder_enabled = Column(Boolean, default=False)
    sold_count = Column(Integer, default=0)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
