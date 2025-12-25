from sqlalchemy import Column, Integer, String, Float, Boolean, ForeignKey
from app.db.base_class import Base

class Product(Base):
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    description = Column(String, nullable=False)
    price = Column(Float, nullable=False)
    discount = Column(Float, default=0.0)
    image_url = Column(String, nullable=False)
    images = Column(String, nullable=True)  # JSON string
    category = Column(String, nullable=False)
    brand = Column(String, nullable=False)
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
