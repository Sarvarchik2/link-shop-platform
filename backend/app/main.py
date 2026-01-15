from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
import os

from app.core.config import settings
from app.db.session import engine
from app.db.base_class import Base

# Import models to ensure they are registered with Base metadata
from app.features.users.models import User
from app.features.shops.models import Shop
from app.features.products.models import Product
from app.features.categories.models import Category
from app.features.brands.models import Brand
from app.features.orders.models import Order, OrderItem
from app.features.subscriptions.models import SubscriptionPlan, SubscriptionRequest
from app.features.banners.models import Banner
from app.features.offers.models import Offer
from app.features.preorders.models import PreOrder

# Import routers
from app.features.auth.router import router as auth_router
from app.features.shops.router import router as shops_router
from app.features.products.router import router as products_router
from app.features.brands.router import router as brands_router
from app.features.categories.router import router as categories_router
from app.features.banners.router import router as banners_router
from app.features.orders.router import router as orders_router
from app.features.media.router import router as media_router
from app.features.subscriptions.router import router as subscriptions_router
from app.features.offers.router import router as offers_router
from app.features.users.router import router as users_router

app = FastAPI(title="Link Shop Platform API")

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://127.0.0.1:3000",
        "http://localhost:8000",
        "http://127.0.0.1:8000",
        "https://link-shop-frontend-production.up.railway.app",
        "https://link-shop-platform-production.up.railway.app",
    ],
    allow_origin_regex=r"https://.*\.up\.railway\.app",
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["*"],
)

# Static files
os.makedirs(settings.UPLOAD_DIR, exist_ok=True)
app.mount("/uploads", StaticFiles(directory=settings.UPLOAD_DIR), name="uploads")

# Include Routers
app.include_router(auth_router, tags=["Authentication"])
app.include_router(users_router, tags=["Users"])
app.include_router(shops_router, tags=["Shops"])
app.include_router(products_router, tags=["Products"])
app.include_router(brands_router, tags=["Brands"])
app.include_router(categories_router, tags=["Categories"])
app.include_router(banners_router, tags=["Banners"])
app.include_router(orders_router, tags=["Orders"])
app.include_router(media_router, tags=["Media"])
app.include_router(subscriptions_router, tags=["Subscriptions"])
app.include_router(offers_router, tags=["Offers"])

@app.on_event("startup")
def on_startup():
    # Create tables
    from sqlalchemy import text
    try:
        db_host = settings.SQLALCHEMY_DATABASE_URI.split("@")[-1].split("/")[0]
        print(f"Startup: Connecting to database host: {db_host}")
    except:
        print("Startup: Connecting to database...")
        
    Base.metadata.create_all(bind=engine)
    
    from sqlalchemy.orm import Session
    from app.db.session import SessionLocal
    from app.features.subscriptions.models import SubscriptionPlan
    from app.features.offers.models import Offer
    
    db = SessionLocal()
    try:
        # Seed Subscription Plans
        if not db.query(SubscriptionPlan).first():
            plans = [
                SubscriptionPlan(
                    name="Пробный период",
                    slug="trial",
                    price=0.0,
                    period_days=30,
                    description="Попробуйте все возможности платформы бесплатно в течение 30 дней",
                    features="Полный доступ к платформе,До 50 товаров,Базовая аналитика",
                    is_trial=True,
                    display_order=1
                ),
                SubscriptionPlan(
                    name="Базовый",
                    slug="basic",
                    price=29.0,
                    period_days=30,
                    description="Идеально для небольших магазинов",
                    features="До 200 товаров,Приоритетная поддержка,Расширенная аналитика",
                    display_order=2
                ),
                SubscriptionPlan(
                    name="Премиум",
                    slug="premium",
                    price=79.0,
                    period_days=30,
                    description="Для растущего бизнеса с большими объемами",
                    features="Безлимитные товары,Личный менеджер,Индивидуальный дизайн",
                    display_order=3
                )
            ]
            for plan in plans:
                db.add(plan)
            db.commit()

        # Seed Offers
        if not db.query(Offer).first():
            offers = [
                Offer(
                    title="Индивидуальный дизайн",
                    description="Разработка уникального стиля для вашего магазина, который выделит вас среди конкурентов.",
                    price_text="от $199",
                    contact_text="Свяжитесь с нами для обсуждения дизайна",
                    contact_email="design@linkshop.com"
                ),
                Offer(
                    title="Приоритетное размещение",
                    description="Ваш магазин будет отображаться первым в общем каталоге платформы.",
                    price=49.0,
                    price_text="$49/мес",
                    contact_text="Активировать прямо сейчас"
                )
            ]
            for offer in offers:
                db.add(offer)
            db.commit()
            
    finally:
        db.close()
    
    # Auto-create admin if env vars are provided (For Railway)
    admin_phone = os.getenv("ADMIN_PHONE")
    admin_password = os.getenv("ADMIN_PASSWORD")
    if admin_phone and admin_password:
        from app.core.security import get_password_hash
        try:
            db = SessionLocal()
            user = db.query(User).filter(User.phone == admin_phone).first()
            if not user:
                print(f"DTO: Auto-creating admin user: {admin_phone}")
                user = User(
                    phone=admin_phone,
                    password_hash=get_password_hash(admin_password),
                    first_name="Platform",
                    last_name="Admin",
                    role="platform_admin"
                )
                db.add(user)
                db.commit()
            else:
                 print(f"DTO: Updating admin user {admin_phone}")
                 user.role = "platform_admin"
                 # Always update password to match env var (in case it changed or was wrong)
                 user.password_hash = get_password_hash(admin_password) 
                 db.commit()
            db.close()
        except Exception as e:
            print(f"DTO: Failed to auto-create admin: {e}")

@app.get("/")
def read_root():
    return {"message": "Welcome to Link Shop Platform API"}
