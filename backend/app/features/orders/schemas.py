from pydantic import BaseModel, ConfigDict
from datetime import datetime
from typing import Optional, List

class OrderItemBase(BaseModel):
    product_id: int
    quantity: int
    selected_color: Optional[str] = None
    selected_size: Optional[str] = None

class OrderItemCreate(OrderItemBase):
    pass

class OrderItemRead(OrderItemBase):
    id: int
    price: float
    order_id: int

    model_config = ConfigDict(from_attributes=True)

class OrderBase(BaseModel):
    delivery_address: str
    delivery_city: str
    delivery_phone: str
    recipient_name: str
    payment_method: str = "cash"
    notes: Optional[str] = None

class OrderCreate(OrderBase):
    items: List[OrderItemCreate]

class OrderRead(OrderBase):
    id: int
    user_id: int
    shop_id: Optional[int] = None
    status: str
    total_price: float
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)

class OrderItemDetail(OrderItemBase):
    price: float
    product_name: str
    product_image: str
    shop_slug: Optional[str] = None

class OrderReadWithItems(OrderRead):
    items: List[OrderItemDetail]

class OrderStatusUpdate(BaseModel):
    status: str
