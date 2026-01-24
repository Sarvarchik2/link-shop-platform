from pydantic import BaseModel, ConfigDict
from datetime import datetime
from typing import Optional

class ShopBase(BaseModel):
    name: str
    slug: str
    description: Optional[str] = None
    logo_url: Optional[str] = None
    email: Optional[str] = None
    phone: Optional[str] = None
    address: Optional[str] = None
    telegram: Optional[str] = None
    instagram: Optional[str] = None
    facebook: Optional[str] = None
    twitter: Optional[str] = None
    whatsapp: Optional[str] = None
    delivery_settings: Optional[dict] = {}

class ShopCreate(ShopBase):
    subscription_plan_id: Optional[int] = None

class ShopUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    logo_url: Optional[str] = None
    email: Optional[str] = None
    phone: Optional[str] = None
    address: Optional[str] = None
    telegram: Optional[str] = None
    instagram: Optional[str] = None
    facebook: Optional[str] = None
    twitter: Optional[str] = None
    whatsapp: Optional[str] = None
    delivery_settings: Optional[dict] = None
    subscription_status: Optional[str] = None
    subscription_expires_at: Optional[datetime] = None
    subscription_plan_id: Optional[int] = None
    telegram_bot_token: Optional[str] = None
    is_bot_active: Optional[bool] = None

class ShopRead(ShopBase):
    id: int
    owner_id: int
    subscription_status: str
    subscription_expires_at: Optional[datetime] = None
    subscription_plan_id: Optional[int] = None
    created_at: datetime
    is_active: bool
    is_bot_active: bool
    auto_renewal_enabled: bool = True
    subscription_period_months: int = 1
    telegram_bot_token: Optional[str] = None # Will be masked on read

    model_config = ConfigDict(from_attributes=True)

class ShopReadWithOwner(ShopRead):
    owner_name: Optional[str] = None
    owner_phone: Optional[str] = None
    subscription_plan_name: Optional[str] = None

class OrdersByStatus(BaseModel):
    pending: int = 0
    processing: int = 0
    shipping: int = 0
    delivered: int = 0
    cancelled: int = 0

class DailyStat(BaseModel):
    date: str
    sales: float = 0.0
    orders: int = 0
    users: int = 0

class PlanStat(BaseModel):
    name: str
    count: int

class ShopRevenueStat(BaseModel):
    id: int
    name: str
    revenue: float
    orders_count: int

class DashboardStats(BaseModel):
    total_sales: float = 0.0
    total_orders: int = 0
    total_users: int = 0
    total_products: int = 0
    orders_by_status: OrdersByStatus
    today_sales: float = 0.0
    today_orders: int = 0
    week_sales: float = 0.0
    week_orders: int = 0
    month_sales: float = 0.0
    month_orders: int = 0
    total_shops: Optional[int] = None
    active_shops: Optional[int] = None
    subscriptions_mrr: Optional[float] = 0.0
    subscriptions_active: Optional[int] = 0
    subscriptions_trial: Optional[int] = 0
    subscriptions_expired: Optional[int] = 0
    plan_limit_products: Optional[int] = None
    plan_limit_banners: Optional[int] = 1
    plan_name: Optional[str] = None
    products_usage_percent: Optional[float] = 0.0
    banners_usage_percent: Optional[float] = 0.0
    total_banners: Optional[int] = 0
    total_broadcasts: Optional[int] = 0
    plan_can_broadcast: Optional[bool] = False
    plan_limit_broadcasts: Optional[int] = None
    history: Optional[list[DailyStat]] = None
    plan_distribution: Optional[list[PlanStat]] = None
    top_shops: Optional[list[ShopRevenueStat]] = None

class AdminActionRequest(BaseModel):
    password: str

class ShopStatusUpdate(BaseModel):
    is_active: bool
    password: str

class TelegramBotTestRequest(BaseModel):
    token: str

class TelegramBotTestResponse(BaseModel):
    valid: bool  # Changed from is_valid to match frontend
    bot_name: Optional[str] = None
    username: Optional[str] = None
    error: Optional[str] = None

class TelegramSyncChatRequest(BaseModel):
    chat_id: str
    init_data: Optional[str] = None

