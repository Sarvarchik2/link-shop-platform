from pydantic import BaseModel, ConfigDict
from datetime import datetime
from typing import Optional, List

class OfferBase(BaseModel):
    title: str
    title_ru: Optional[str] = None
    title_en: Optional[str] = None
    title_uz: Optional[str] = None
    
    description: str
    description_ru: Optional[str] = None
    description_en: Optional[str] = None
    description_uz: Optional[str] = None
    
    price: Optional[float] = None
    price_text: Optional[str] = None
    price_text_ru: Optional[str] = None
    price_text_en: Optional[str] = None
    price_text_uz: Optional[str] = None
    
    contact_text: str = "Свяжитесь с нами для покупки"
    contact_text_ru: Optional[str] = None
    contact_text_en: Optional[str] = None
    contact_text_uz: Optional[str] = None
    
    contact_email: Optional[str] = None
    contact_phone: Optional[str] = None
    is_active: bool = True
    display_order: int = 0

class OfferCreate(OfferBase):
    pass

class OfferUpdate(BaseModel):
    title: Optional[str] = None
    title_ru: Optional[str] = None
    title_en: Optional[str] = None
    title_uz: Optional[str] = None
    
    description: Optional[str] = None
    description_ru: Optional[str] = None
    description_en: Optional[str] = None
    description_uz: Optional[str] = None
    
    price: Optional[float] = None
    price_text: Optional[str] = None
    price_text_ru: Optional[str] = None
    price_text_en: Optional[str] = None
    price_text_uz: Optional[str] = None
    
    contact_text: Optional[str] = None
    contact_text_ru: Optional[str] = None
    contact_text_en: Optional[str] = None
    contact_text_uz: Optional[str] = None
    
    contact_email: Optional[str] = None
    contact_phone: Optional[str] = None
    is_active: Optional[bool] = None
    display_order: Optional[int] = None

class OfferRead(OfferBase):
    id: int
    created_at: datetime
    model_config = ConfigDict(from_attributes=True)
