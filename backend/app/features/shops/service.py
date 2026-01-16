from sqlalchemy.orm import Session
from fastapi import HTTPException
from .repository import ShopRepository
from .models import Shop
from datetime import datetime, timedelta
from app.features.products.models import Product
from app.features.orders.models import Order
from app.features.users.models import User
from app.features.banners.models import Banner
from .schemas import ShopCreate, ShopUpdate, DashboardStats, OrdersByStatus

from app.features.subscriptions.models import SubscriptionPlan, SubscriptionRequest
import httpx
from app.core.crypto import crypto
from .models import Shop, UserStoreTelegram
from .schemas import ShopCreate, ShopUpdate, DashboardStats, OrdersByStatus, TelegramBotTestResponse

class ShopService:
    def __init__(self):
        self.repository = ShopRepository()

    def get_shop_by_slug(self, db: Session, slug: str, check_active: bool = False):
        shop = self.repository.get_by_slug(db, slug)
        if not shop:
            raise HTTPException(status_code=404, detail="Shop not found")
        
        if check_active:
            if not shop.is_active:
                raise HTTPException(status_code=403, detail="Shop is not active")
            if shop.subscription_status == "expired" or (shop.subscription_expires_at and shop.subscription_expires_at < datetime.utcnow()):
                raise HTTPException(status_code=403, detail="Shop subscription expired")
        
        return shop

    def get_shop_by_id(self, db: Session, shop_id: int, check_active: bool = False):
        shop = self.repository.get_by_id(db, shop_id)
        if not shop:
            raise HTTPException(status_code=404, detail="Shop not found")
        
        if check_active:
            if not shop.is_active:
                raise HTTPException(status_code=403, detail="Shop is not active")
            if shop.subscription_status == "expired" or (shop.subscription_expires_at and shop.subscription_expires_at < datetime.utcnow()):
                raise HTTPException(status_code=403, detail="Shop subscription expired")
        
        return shop


    def register_shop(self, db: Session, shop_in: ShopCreate, owner_id: int):
        # Check if user already has a shop
        existing_user_shop = self.repository.get_by_owner_id(db, owner_id)
        if existing_user_shop:
            raise HTTPException(status_code=400, detail="User already has a shop")
        
        # Check if slug is taken
        existing_shop = self.repository.get_by_slug(db, shop_in.slug)
        if existing_shop:
            raise HTTPException(status_code=400, detail="Shop slug already taken")
        
        shop_data = shop_in.model_dump()
        shop_data["owner_id"] = owner_id
        
        # Handle subscription logic
        requested_plan_id = shop_data.get("subscription_plan_id")
        pending_plan_request = None
        
        if requested_plan_id:
            requested_plan = db.query(SubscriptionPlan).filter(SubscriptionPlan.id == requested_plan_id).first()
            
            if requested_plan:
                if requested_plan.price > 0:
                    # Paid plan: Give Trial (7 days) on Free plan (or None)
                    free_plan = db.query(SubscriptionPlan).filter(SubscriptionPlan.price == 0).first()
                    
                    # Store requested plan ID for creating request later
                    pending_plan_request = requested_plan.id
                    
                    # Set shop to Free/Trial
                    shop_data["subscription_plan_id"] = free_plan.id if free_plan else None
                    shop_data["subscription_status"] = "trial"
                    shop_data["subscription_expires_at"] = datetime.utcnow() + timedelta(days=7)
                else:
                    # Free plan: Activate immediately
                    shop_data["subscription_status"] = "active"
                    # Default to 1 month for now, or longer for free? Let's say 30 days renewable or long term. 
                    # If it's truly free, expiry might not matter as much, but let's set it.
                    period = requested_plan.period_days if requested_plan.period_days else 30
                    shop_data["subscription_expires_at"] = datetime.utcnow() + timedelta(days=period)
        
        # Ensure subscription info is handled if not set above
        if "subscription_plan_id" not in shop_data:
             shop_data["subscription_plan_id"] = None

        new_shop = self.repository.create(db, shop_data)
        
        # Create Subscription Request if it was a paid plan
        if pending_plan_request:
            new_request = SubscriptionRequest(
                shop_id=new_shop.id,
                plan_id=pending_plan_request,
                type="new",
                status="pending",
                duration_months=1, # Default to 1 month for initial request
                requested_at=datetime.utcnow()
            )
            db.add(new_request)
            db.commit()
            
        return new_shop

    def update_shop(self, db: Session, slug: str, shop_in: ShopUpdate, current_user):
        check_active = (current_user.role != "platform_admin")
        shop = self.get_shop_by_slug(db, slug, check_active=check_active)
        
        # Check permissions
        if current_user.role != "platform_admin" and shop.owner_id != current_user.id:
            raise HTTPException(status_code=403, detail="Not authorized")
            
        update_data = shop_in.model_dump(exclude_unset=True)
        
        # Handle Telegram Bot Token encryption
        if "telegram_bot_token" in update_data and update_data["telegram_bot_token"]:
             # If it's a new token (not masked)
             if not update_data["telegram_bot_token"].endswith("..."):
                 update_data["telegram_bot_token"] = crypto.encrypt(update_data["telegram_bot_token"])
        
        return self.repository.update(db, shop, update_data)

    async def verify_bot_token(self, token: str) -> TelegramBotTestResponse:
        async with httpx.AsyncClient() as client:
            try:
                response = await client.get(f"https://api.telegram.org/bot{token}/getMe")
                if response.status_code == 200:
                    data = response.json()
                    return TelegramBotTestResponse(is_valid=True, bot_info=data.get("result"))
                else:
                    return TelegramBotTestResponse(is_valid=False, error=response.json().get("description", "Unknown error"))
            except Exception as e:
                return TelegramBotTestResponse(is_valid=False, error=str(e))

    def sync_telegram_chat(self, db: Session, shop_slug: str, user_id: int, chat_id: str):
        shop = self.get_shop_by_slug(db, shop_slug)
        mapping = db.query(UserStoreTelegram).filter(
            UserStoreTelegram.user_id == user_id,
            UserStoreTelegram.store_id == shop.id
        ).first()
        
        if mapping:
            mapping.telegram_chat_id = chat_id
        else:
            mapping = UserStoreTelegram(
                user_id=user_id,
                store_id=shop.id,
                telegram_chat_id=chat_id
            )
            db.add(mapping)
        
        db.commit()
        return mapping


    def get_all_shops_for_admin(self, db: Session):
        shops_with_owners = self.repository.get_all_with_owners(db)
        result = []
        for shop, first_name, last_name, phone, plan_name in shops_with_owners:
            shop_data = {
                **shop.__dict__,
                "owner_name": f"{first_name} {last_name}",
                "owner_phone": phone,
                "subscription_plan_name": plan_name or "Нет плана"
            }
            # Remove SQLAlchemy internal state
            shop_data.pop("_sa_instance_state", None)
            result.append(shop_data)
        return result

    def get_shop_details_for_admin(self, db: Session, shop_id: int):
        # We need to join with User and SubscriptionPlan
        result = db.query(Shop, User.first_name, User.last_name, User.phone, SubscriptionPlan.name)\
            .join(User, Shop.owner_id == User.id)\
            .outerjoin(SubscriptionPlan, Shop.subscription_plan_id == SubscriptionPlan.id)\
            .filter(Shop.id == shop_id)\
            .first()
            
        if not result:
             raise HTTPException(status_code=404, detail="Shop not found")
        
        shop, first_name, last_name, phone, plan_name = result
        
        shop_data = {
            **shop.__dict__,
            "owner_name": f"{first_name} {last_name}",
            "owner_phone": phone,
            "subscription_plan_name": plan_name or "Нет плана"
        }
        shop_data.pop("_sa_instance_state", None)
        return shop_data

    def _mask_token(self, encrypted_token: str) -> str:
        if not encrypted_token:
            return None
        token = crypto.decrypt(encrypted_token)
        if not token or ":" not in token:
            return "Invalid Token"
        parts = token.split(":")
        prefix = parts[0]
        suffix = parts[1]
        return f"{prefix}:{suffix[:4]}...{suffix[-4:]}"

    def prepare_for_read(self, shop: Shop) -> Shop:
        """Mask sensitive info before sending to client"""
        if shop.telegram_bot_token:
            shop.telegram_bot_token = self._mask_token(shop.telegram_bot_token)
        return shop


    def get_my_shops(self, db: Session, user_id: int):
        return self.repository.get_by_owner_id(db, user_id)

    def get_shop_stats(self, db: Session, shop_slug: str, current_user):
        shop = self.get_shop_by_slug(db, shop_slug)
        
        # Check permissions
        if current_user.role != "platform_admin" and shop.owner_id != current_user.id:
            raise HTTPException(status_code=403, detail="Not authorized")
            
        # Get products count
        total_products = db.query(Product).filter(Product.shop_id == shop.id).count()
        
        # Get orders
        orders = db.query(Order).filter(Order.shop_id == shop.id).all()
        total_orders = len(orders)
        
        # Unique users
        user_ids = set(o.user_id for o in orders)
        total_users = len(user_ids)
        
        # Sales
        total_sales = sum(o.total_price for o in orders if o.status != "cancelled")
        
        # Orders by status
        orders_by_status = OrdersByStatus(
            pending=sum(1 for o in orders if o.status == "pending"),
            processing=sum(1 for o in orders if o.status == "processing"),
            shipping=sum(1 for o in orders if o.status == "shipping"),
            delivered=sum(1 for o in orders if o.status == "delivered"),
            cancelled=sum(1 for o in orders if o.status == "cancelled")
        )
        
        # Time-based stats
        now = datetime.utcnow()
        today_start = now.replace(hour=0, minute=0, second=0, microsecond=0)
        week_start = today_start - timedelta(days=now.weekday())
        month_start = now.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
        
        today_orders_list = [o for o in orders if o.created_at >= today_start and o.status != "cancelled"]
        week_orders_list = [o for o in orders if o.created_at >= week_start and o.status != "cancelled"]
        month_orders_list = [o for o in orders if o.created_at >= month_start and o.status != "cancelled"]
        
        month_orders_list = [o for o in orders if o.created_at >= month_start and o.status != "cancelled"]
        
        # Get Subscription Limits
        plan = db.query(SubscriptionPlan).filter(SubscriptionPlan.id == shop.subscription_plan_id).first()
        plan_limit_products = plan.max_products if plan else None
        plan_name = plan.name if plan else None
        
        products_usage_percent = 0.0
        if plan_limit_products and plan_limit_products > 0:
            products_usage_percent = (total_products / plan_limit_products) * 100
            if products_usage_percent > 100: products_usage_percent = 100.0

        # Feature: Banners
        total_banners = db.query(Banner).filter(Banner.shop_id == shop.id).count()
        plan_limit_banners = plan.max_banners if plan else 1
        
        banners_usage_percent = 0.0
        if plan_limit_banners and plan_limit_banners > 0:
            banners_usage_percent = (total_banners / plan_limit_banners) * 100
            if banners_usage_percent > 100: banners_usage_percent = 100.0

        return DashboardStats(
            total_sales=total_sales,
            total_orders=total_orders,
            total_users=total_users,
            total_products=total_products,
            orders_by_status=orders_by_status,
            today_sales=sum(o.total_price for o in today_orders_list),
            today_orders=len(today_orders_list),
            week_sales=sum(o.total_price for o in week_orders_list),
            week_orders=len(week_orders_list),
            month_sales=sum(o.total_price for o in month_orders_list),
            month_orders=len(month_orders_list),
            plan_limit_products=plan_limit_products,
            plan_name=plan_name,
            plan_limit_banners=plan_limit_banners,
            products_usage_percent=products_usage_percent,
            banners_usage_percent=banners_usage_percent,
            total_banners=total_banners
        )

    def get_platform_stats(self, db: Session):
        from sqlalchemy import func
        
        total_shops = db.query(Shop).count()
        active_shops = db.query(Shop).filter(Shop.is_active == True).count()
        
        total_users = db.query(User).count()
        total_products = db.query(Product).count()
        
        # Orders statistics
        orders_query = db.query(Order).filter(Order.status != "cancelled")
        total_orders = db.query(Order).count()
        total_sales = db.query(func.sum(Order.total_price)).filter(Order.status != "cancelled").scalar() or 0.0
        
        orders_by_status = OrdersByStatus(
            pending=db.query(Order).filter(Order.status == "pending").count(),
            processing=db.query(Order).filter(Order.status == "processing").count(),
            shipping=db.query(Order).filter(Order.status == "shipping").count(),
            delivered=db.query(Order).filter(Order.status == "delivered").count(),
            cancelled=db.query(Order).filter(Order.status == "cancelled").count()
        )
        
        now = datetime.utcnow()
        today_start = now.replace(hour=0, minute=0, second=0, microsecond=0)
        week_start = today_start - timedelta(days=now.weekday())
        month_start = now.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
        
        today_sales = db.query(func.sum(Order.total_price)).filter(Order.created_at >= today_start, Order.status != "cancelled").scalar() or 0.0
        today_orders = db.query(Order).filter(Order.created_at >= today_start, Order.status != "cancelled").count()
        
        week_sales = db.query(func.sum(Order.total_price)).filter(Order.created_at >= week_start, Order.status != "cancelled").scalar() or 0.0
        week_orders = db.query(Order).filter(Order.created_at >= week_start, Order.status != "cancelled").count()
        
        month_sales = db.query(func.sum(Order.total_price)).filter(Order.created_at >= month_start, Order.status != "cancelled").scalar() or 0.0
        month_orders = db.query(Order).filter(Order.created_at >= month_start, Order.status != "cancelled").count()
        
        # Subscription Stats
        subscriptions_active = db.query(Shop).filter(Shop.subscription_status == 'active').count()
        subscriptions_trial = db.query(Shop).filter(Shop.subscription_status == 'trial').count()
        subscriptions_expired = db.query(Shop).filter(Shop.subscription_status == 'expired').count()
        
        # Calculate MRR
        # We need plan prices
        plans = db.query(SubscriptionPlan).all()
        plan_prices = {p.id: p.price for p in plans}
        
        subscriptions_mrr = 0.0
        active_shops_list = db.query(Shop).filter(Shop.subscription_status == 'active').all()
        for s in active_shops_list:
            if s.subscription_plan_id in plan_prices:
                subscriptions_mrr += plan_prices[s.subscription_plan_id]
        
        return DashboardStats(
            total_sales=total_sales,
            total_orders=total_orders,
            total_users=total_users,
            total_products=total_products,
            orders_by_status=orders_by_status,
            today_sales=today_sales,
            today_orders=today_orders,
            week_sales=week_sales,
            week_orders=week_orders,
            month_sales=month_sales,
            month_orders=month_orders,
            total_shops=total_shops,
            active_shops=active_shops,
            subscriptions_mrr=subscriptions_mrr,
            subscriptions_active=subscriptions_active,
            subscriptions_trial=subscriptions_trial,
            subscriptions_expired=subscriptions_expired
        )

    def delete_shop(self, db: Session, shop_id: int):
        shop = self.get_shop_by_id(db, shop_id)
        self.repository.delete(db, shop)
