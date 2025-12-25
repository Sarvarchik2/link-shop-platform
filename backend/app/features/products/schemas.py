from pydantic import BaseModel, ConfigDict
from typing import Optional, List

class ProductBase(BaseModel):
    name: str
    description: str
    price: float
    discount: float = 0.0
    image_url: str
    images: Optional[str] = None
    category: str
    brand: str
    stock: int = 0
    sizes: Optional[str] = None
    colors: Optional[str] = None
    variants: Optional[str] = None
    is_preorder_enabled: bool = False

class ProductCreate(ProductBase):
    pass

class ProductUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    price: Optional[float] = None
    discount: Optional[float] = None
    image_url: Optional[str] = None
    images: Optional[str] = None
    category: Optional[str] = None
    brand: Optional[str] = None
    stock: Optional[int] = None
    sizes: Optional[str] = None
    colors: Optional[str] = None
    variants: Optional[str] = None
    is_preorder_enabled: Optional[bool] = None

class ProductRead(ProductBase):
    id: int
    rating: float
    reviews_count: int
    is_favorite: bool
    sold_count: int
    shop_id: Optional[int] = None

    model_config = ConfigDict(from_attributes=True)
