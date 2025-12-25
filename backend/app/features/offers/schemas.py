from pydantic import BaseModel, ConfigDict
from datetime import datetime
from typing import Optional, List

class OfferBase(BaseModel):
    title: str
    description: str
    price: Optional[float] = None
    price_text: Optional[str] = None
    contact_text: str = "Свяжитесь с нами для покупки"
    contact_email: Optional[str] = None
    contact_phone: Optional[str] = None
    is_active: bool = True
    display_order: int = 0

class OfferCreate(OfferBase):
    pass

class OfferRead(OfferBase):
    id: int
    created_at: datetime
    model_config = ConfigDict(from_attributes=True)
