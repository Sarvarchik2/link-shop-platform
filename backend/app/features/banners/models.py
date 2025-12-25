from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from app.db.base_class import Base

class Banner(Base):
    id = Column(Integer, primary_key=True, index=True)
    badge_text = Column(String, default="NEW ARRIVAL")
    title = Column(String, default="Ray-Ban Meta Smart Glasses")
    subtitle = Column(String, default="Starting from $299")
    button_text = Column(String, default="Shop Now")
    button_link = Column(String, default="/products")
    image_url = Column(String, default="")
    is_active = Column(Boolean, default=True)
    shop_id = Column(Integer, ForeignKey("shop.id"), nullable=True)
