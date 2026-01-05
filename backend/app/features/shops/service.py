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

from app.features.subscriptions.models import SubscriptionPlan

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
        
        # Ensure subscription info is handled
        if "subscription_plan_id" not in shop_data:
             shop_data["subscription_plan_id"] = None

        return self.repository.create(db, shop_data)

    def update_shop(self, db: Session, slug: str, shop_in: ShopUpdate, current_user):
        check_active = (current_user.role != "platform_admin")
        shop = self.get_shop_by_slug(db, slug, check_active=check_active)
        
        # Check permissions
        if current_user.role != "platform_admin" and shop.owner_id != current_user.id:
            raise HTTPException(status_code=403, detail="Not authorized")
            
        update_data = shop_in.model_dump(exclude_unset=True)
        return self.repository.update(db, shop, update_data)

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
        shops = db.query(Shop).all()
        total_shops = len(shops)
        active_shops = len([s for s in shops if s.is_active])
        
        users = db.query(User).all()
        total_users = len(users)
        
        products = db.query(Product).all()
        total_products = len(products)
        
        orders = db.query(Order).all()
        total_orders = len(orders)
        
        total_sales = sum(o.total_price for o in orders if o.status != "cancelled")
        
        orders_by_status = OrdersByStatus(
            pending=sum(1 for o in orders if o.status == "pending"),
            processing=sum(1 for o in orders if o.status == "processing"),
            shipping=sum(1 for o in orders if o.status == "shipping"),
            delivered=sum(1 for o in orders if o.status == "delivered"),
            cancelled=sum(1 for o in orders if o.status == "cancelled")
        )
        
        now = datetime.utcnow()
        today_start = now.replace(hour=0, minute=0, second=0, microsecond=0)
        week_start = today_start - timedelta(days=now.weekday())
        month_start = now.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
        
        today_orders_list = [o for o in orders if o.created_at >= today_start and o.status != "cancelled"]
        week_orders_list = [o for o in orders if o.created_at >= week_start and o.status != "cancelled"]
        month_orders_list = [o for o in orders if o.created_at >= month_start and o.status != "cancelled"]
        
        month_orders_list = [o for o in orders if o.created_at >= month_start and o.status != "cancelled"]
        
        # Subscription Stats
        subscriptions_active = 0
        subscriptions_trial = 0
        subscriptions_expired = 0
        subscriptions_mrr = 0.0
        
        # Helper map for plan prices
        plans = db.query(SubscriptionPlan).all()
        plan_prices = {p.id: p.price for p in plans}
        
        for s in shops:
            if s.subscription_status == 'active':
                subscriptions_active += 1
                if s.subscription_plan_id in plan_prices:
                    subscriptions_mrr += plan_prices[s.subscription_plan_id]
            elif s.subscription_status == 'trial':
                subscriptions_trial += 1
            elif s.subscription_status == 'expired':
                subscriptions_expired += 1
        
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
