from pydantic import BaseModel, ConfigDict
from typing import Optional, List

class ProductBase(BaseModel):
    # Multilingual fields
    name_uz: str
    name_ru: str
    name_en: str
    
    description_uz: str
    description_ru: str
    description_en: str
    
    price: float
    discount: float = 0.0
    image_url: str
    images: Optional[str] = None
    
    category_uz: str
    category_ru: str
    category_en: str
    
    brand_uz: str
    brand_ru: str
    brand_en: str
    
    stock: int = 0
    sizes: Optional[str] = None
    colors: Optional[str] = None
    variants: Optional[str] = None
    is_preorder_enabled: bool = False

class ProductCreate(ProductBase):
    pass

class ProductUpdate(BaseModel):
    name_uz: Optional[str] = None
    name_ru: Optional[str] = None
    name_en: Optional[str] = None
    
    description_uz: Optional[str] = None
    description_ru: Optional[str] = None
    description_en: Optional[str] = None
    
    price: Optional[float] = None
    discount: Optional[float] = None
    image_url: Optional[str] = None
    images: Optional[str] = None
    
    category_uz: Optional[str] = None
    category_ru: Optional[str] = None
    category_en: Optional[str] = None
    
    brand_uz: Optional[str] = None
    brand_ru: Optional[str] = None
    brand_en: Optional[str] = None
    
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
