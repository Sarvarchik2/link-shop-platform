from pydantic import BaseModel, ConfigDict, field_validator
from datetime import datetime
from typing import Optional, List

class SubscriptionPlanBase(BaseModel):
    name: str
    name_ru: Optional[str] = None
    name_en: Optional[str] = None
    name_uz: Optional[str] = None
    
    slug: str
    price: float
    period_days: int = 30
    
    description: Optional[str] = None
    description_ru: Optional[str] = None
    description_en: Optional[str] = None
    description_uz: Optional[str] = None
    
    features: Optional[str] = None
    features_ru: Optional[str] = None
    features_en: Optional[str] = None
    features_uz: Optional[str] = None
    
    is_active: bool = True
    is_trial: bool = False
    display_order: int = 0
    max_products: Optional[int] = None
    max_banners: Optional[int] = 1
    can_broadcast: bool = False
    has_telegram: bool = False

class SubscriptionPlanCreate(SubscriptionPlanBase):
    pass

class SubscriptionPlanUpdate(BaseModel):
    name: Optional[str] = None
    name_ru: Optional[str] = None
    name_en: Optional[str] = None
    name_uz: Optional[str] = None
    
    slug: Optional[str] = None
    price: Optional[float] = None
    period_days: Optional[int] = None
    
    description: Optional[str] = None
    description_ru: Optional[str] = None
    description_en: Optional[str] = None
    description_uz: Optional[str] = None
    
    features: Optional[str] = None
    features_ru: Optional[str] = None
    features_en: Optional[str] = None
    features_uz: Optional[str] = None
    
    is_active: Optional[bool] = None
    is_trial: Optional[bool] = None
    display_order: Optional[int] = None
    max_products: Optional[int] = None
    max_banners: Optional[int] = None
    can_broadcast: Optional[bool] = None
    has_telegram: Optional[bool] = None

class SubscriptionPlanRead(SubscriptionPlanBase):
    id: int
    created_at: datetime
    features_list: List[str] = []

    model_config = ConfigDict(from_attributes=True)

    @field_validator('features_list', mode='before')
    @classmethod
    def split_features(cls, v, info):
        # info.data might not have 'features' yet because it's populated during model parsing
        # but we can handle it if 'v' is empty and features is in the source object
        return v

class SubscriptionRequestBase(BaseModel):
    plan_id: int
    duration_months: int = 1
    type: str = "new" # new, renew, change
    notes: Optional[str] = None

class SubscriptionRequestCreate(SubscriptionRequestBase):
    pass

class SubscriptionRequestUpdate(BaseModel):
    status: Optional[str] = None
    notes: Optional[str] = None

class SubscriptionRequestRead(SubscriptionRequestBase):
    id: int
    shop_id: int
    status: str
    requested_at: datetime
    approved_at: Optional[datetime] = None
    plan_name: Optional[str] = None
    shop_name: Optional[str] = None
    shop_slug: Optional[str] = None
    
    model_config = ConfigDict(from_attributes=True)


# New schemas for wallet-based subscription purchase
class SubscriptionPurchaseRequest(BaseModel):
    plan_slug: str
    period_months: int = 1  # 1, 3, 6, 12
    payment_method: str = "wallet"  # wallet, payme

class SubscriptionPurchaseResponse(BaseModel):
    success: bool
    subscription_id: Optional[int] = None
    expires_at: Optional[datetime] = None
    message: str

class AutoRenewalToggleRequest(BaseModel):
    enabled: bool

class AutoRenewalToggleResponse(BaseModel):
    auto_renewal_enabled: bool
    message: str

