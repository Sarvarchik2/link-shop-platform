from sqlalchemy import Column, Integer, String, ForeignKey
from app.db.base_class import Base

class Brand(Base):
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    logo_url = Column(String, nullable=False)
    shop_id = Column(Integer, ForeignKey("shop.id"), nullable=True)
