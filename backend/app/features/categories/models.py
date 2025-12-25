from sqlalchemy import Column, Integer, String, ForeignKey
from app.db.base_class import Base

class Category(Base):
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    image_url = Column(String, nullable=True)
    shop_id = Column(Integer, ForeignKey("shop.id"), nullable=True)
