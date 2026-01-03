from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from app.db.base_class import Base

class Banner(Base):
    id = Column(Integer, primary_key=True, index=True)
    badge_text = Column(String, default="NEW ARRIVAL")
    
    # Multilingual Title
    title_ru = Column(String, nullable=True)
    title_en = Column(String, nullable=True)
    title_uz = Column(String, nullable=True)
    # Deprecated single field, keeping for backward compat or fallback
    title = Column(String, default="Ray-Ban Meta Smart Glasses") 

    # Multilingual Subtitle
    subtitle_ru = Column(String, nullable=True)
    subtitle_en = Column(String, nullable=True)
    subtitle_uz = Column(String, nullable=True)
    subtitle = Column(String, default="Starting from $299")

    # Multilingual Button Text
    button_text_ru = Column(String, nullable=True)
    button_text_en = Column(String, nullable=True)
    button_text_uz = Column(String, nullable=True)
    button_text = Column(String, default="Shop Now")

    button_link = Column(String, default="/products")
    image_url = Column(String, default="")
    is_active = Column(Boolean, default=True)
    shop_id = Column(Integer, ForeignKey("shop.id"), nullable=True)
