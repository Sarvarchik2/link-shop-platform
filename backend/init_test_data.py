#!/usr/bin/env python3
"""
Script for clearing database and creating test data:
- Shop owner with fully configured shop (Premium Eyewear)
- Regular user
- Platform admin
"""

import os
import json
from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, text
from app.db.base_class import Base
from app.core.security import get_password_hash
from app.core.config import settings
from app.db.session import engine

# Import Models
from app.features.users.models import User
from app.features.shops.models import Shop
from app.features.products.models import Product
from app.features.brands.models import Brand
from app.features.categories.models import Category
from app.features.banners.models import Banner
from app.features.subscriptions.models import SubscriptionPlan

def clear_database():
    """Drops all tables to clear data"""
    if "sqlite" in settings.DATABASE_URL:
        db_file = settings.DATABASE_URL.replace("sqlite:///", "")
        if os.path.exists(db_file):
            os.remove(db_file)
            print("✓ SQLite database file removed")
    else:
        # For Postgres, we drop schema to handle cascades appropriately
        with engine.connect() as connection:
            connection.execute(text("DROP SCHEMA public CASCADE"))
            connection.execute(text("CREATE SCHEMA public"))
            connection.commit()
        print("✓ Tables dropped (Schema reset)")

def create_tables():
    """Creates all tables"""
    Base.metadata.create_all(engine)
    print("✓ Tables created")

def init_test_data():
    """Create test data"""
    with Session(engine) as session:
        # 1. Create platform admin
        admin = User(
            phone="998900000000",
            password_hash=get_password_hash("admin123"),
            first_name="Admin",
            last_name="System",
            role="platform_admin"
        )
        session.add(admin)
        session.commit()
        session.refresh(admin)
        print("✓ Platform admin created: 998900000000 / admin123")
        
        # 2. Create shop owner
        shop_owner = User(
            phone="998901234567",
            password_hash=get_password_hash("owner123"),
            first_name="Ivan",
            last_name="Petrov",
            role="shop_owner"
        )
        session.add(shop_owner)
        session.commit()
        session.refresh(shop_owner)
        print("✓ Shop owner created: 998901234567 / owner123")
        
        # ... (skip shop creation lines as they don't change owner_id reference logic)
        
        # 3. Create shop
        subscription_expires = datetime.utcnow() + timedelta(days=365)
        shop = Shop(
            name="Premium Eyewear Store",
            slug="premium-eyewear",
            owner_id=shop_owner.id,
            description="Premium eyewear store featuring luxury brands and smart glasses.",
            logo_url="https://images.unsplash.com/photo-1572635196237-14b3f281503f?q=80&w=200&auto=format&fit=crop",
            subscription_status="active",
            subscription_expires_at=subscription_expires,
            is_active=True,
            phone="+998901234567",
            email="info@eyewear.uz",
            address="Tashkent, Amir Temur 1"
        )
        session.add(shop)
        session.commit()
        session.refresh(shop)
        print("✓ Shop created: Premium Eyewear Store")
        
        # 4. Create brands
        brands = [
            Brand(name="Ray-Ban", logo_url="https://upload.wikimedia.org/wikipedia/commons/thumb/0/03/Ray-Ban_logo.svg/2560px-Ray-Ban_logo.svg.png", shop_id=shop.id),
            Brand(name="Oakley", logo_url="https://upload.wikimedia.org/wikipedia/commons/thumb/f/f6/Oakley_logo.svg/2560px-Oakley_logo.svg.png", shop_id=shop.id),
            Brand(name="Prada", logo_url="https://upload.wikimedia.org/wikipedia/commons/thumb/b/b8/Prada-Logo.svg/2560px-Prada-Logo.svg.png", shop_id=shop.id),
            Brand(name="Gucci", logo_url="https://upload.wikimedia.org/wikipedia/commons/thumb/7/79/Gucci_Logo.svg/2560px-Gucci_Logo.svg.png", shop_id=shop.id),
            Brand(name="Tom Ford", logo_url="https://upload.wikimedia.org/wikipedia/commons/thumb/9/9a/Tom_Ford_logo.svg/2560px-Tom_Ford_logo.svg.png", shop_id=shop.id),
        ]
        session.add_all(brands)
        session.commit()
        print("✓ Brands created")
        
        # 5. Create categories (multilingual)
        categories = [
            Category(
                name_ru="Солнцезащитные очки", 
                name_en="Sunglasses", 
                name_uz="Quyosh ko'zoynaklari",
                image_url="https://images.unsplash.com/photo-1511499767150-a48a237f0083?q=80&w=600&auto=format&fit=crop", 
                shop_id=shop.id
            ),
            Category(
                name_ru="Умные очки", 
                name_en="Smart Glasses", 
                name_uz="Aqlli ko'zoynaklar",
                image_url="https://images.unsplash.com/photo-1572635196237-14b3f281503f?q=80&w=600&auto=format&fit=crop", 
                shop_id=shop.id
            ),
            Category(
                name_ru="Очки для зрения", 
                name_en="Eyeglasses", 
                name_uz="Ko'rish ko'zoynaklari",
                image_url="https://images.unsplash.com/photo-1577803645773-f96470509666?q=80&w=600&auto=format&fit=crop", 
                shop_id=shop.id
            ),
            Category(
                name_ru="Люксовые очки", 
                name_en="Luxury Eyewear", 
                name_uz="Lyuks ko'zoynaklar",
                image_url="https://images.unsplash.com/photo-1511499767150-a48a237f0083?q=80&w=600&auto=format&fit=crop", 
                shop_id=shop.id
            ),
            Category(
                name_ru="Спортивные очки", 
                name_en="Sports Eyewear", 
                name_uz="Sport ko'zoynaklari",
                image_url="https://images.unsplash.com/photo-1572635196237-14b3f281503f?q=80&w=600&auto=format&fit=crop", 
                shop_id=shop.id
            ),
        ]
        session.add_all(categories)
        session.commit()
        print("✓ Categories created")
        
        # 6. Create products (multilingual)
        products = [
            Product(
                name_ru="Ray-Ban Meta Wayfarer",
                name_en="Ray-Ban Meta Wayfarer",
                name_uz="Ray-Ban Meta Wayfarer",
                description_ru="Классический стиль Wayfarer с умными функциями. Встроенная камера, динамики и ИИ.",
                description_en="Classic Wayfarer style with smart features. Built-in camera, speakers and AI.",
                description_uz="Aqlli funksiyalarga ega klassik Wayfarer uslubi. O'rnatilgan kamera, dinamiklar va sun'iy intellekt.",
                price=299.00,
                image_url="https://images.unsplash.com/photo-1572635196237-14b3f281503f?q=80&w=2080&auto=format&fit=crop",
                images=json.dumps([
                    "https://images.unsplash.com/photo-1572635196237-14b3f281503f?q=80&w=2080&auto=format&fit=crop",
                    "https://images.unsplash.com/photo-1511499767150-a48a237f0083?q=80&w=2080&auto=format&fit=crop"
                ]),
                # Multilingual string fields for filtering
                category_ru="Умные очки", category_en="Smart Glasses", category_uz="Aqlli ko'zoynaklar",
                brand_ru="Ray-Ban", brand_en="Ray-Ban", brand_uz="Ray-Ban",
                rating=4.8, reviews_count=156, stock=15,
                variants=json.dumps([
                    {"size": "M", "color": "Black", "colorHex": "#000000", "stock": 5},
                    {"size": "L", "color": "Black", "colorHex": "#000000", "stock": 2}
                ]),
                shop_id=shop.id
            ),
            Product(
                name_ru="Ray-Ban Aviator Classic",
                name_en="Ray-Ban Aviator Classic",
                name_uz="Ray-Ban Aviator Classic",
                description_ru="Легендарный стиль авиатор. Золотая оправа и зеленые линзы.",
                description_en="Legendary aviator style. Gold frame and green lenses.",
                description_uz="Afsonaviy aviator uslubi. Oltin ramka va yashil linzalar.",
                price=163.00,
                image_url="https://images.unsplash.com/photo-1511499767150-a48a237f0083?q=80&w=2080&auto=format&fit=crop",
                images=json.dumps([
                    "https://images.unsplash.com/photo-1511499767150-a48a237f0083?q=80&w=2080&auto=format&fit=crop"
                ]),
                category_ru="Солнцезащитные очки", category_en="Sunglasses", category_uz="Quyosh ko'zoynaklari",
                brand_ru="Ray-Ban", brand_en="Ray-Ban", brand_uz="Ray-Ban",
                rating=4.7, reviews_count=242, stock=35,
                variants=json.dumps([
                    {"size": "M", "color": "Gold", "colorHex": "#FFD700", "stock": 10},
                    {"size": "L", "color": "Gold", "colorHex": "#FFD700", "stock": 8}
                ]),
                shop_id=shop.id
            ),
            Product(
                name_ru="Oakley Holbrook",
                name_en="Oakley Holbrook",
                name_uz="Oakley Holbrook",
                description_ru="Вневременной классический дизайн с современными технологиями линз Prizm.",
                description_en="Timeless classic design with modern Prizm lens technology.",
                description_uz="Zamonaviy Prizm linza texnologiyasi bilan birlashtirilgan o'zgarmas klassik dizayn.",
                price=152.00,
                image_url="https://images.unsplash.com/photo-1577803645773-f96470509666?q=80&w=2080&auto=format&fit=crop",
                images=json.dumps([
                     "https://images.unsplash.com/photo-1577803645773-f96470509666?q=80&w=2080&auto=format&fit=crop"
                ]),
                category_ru="Спортивные очки", category_en="Sports Eyewear", category_uz="Sport ko'zoynaklari",
                brand_ru="Oakley", brand_en="Oakley", brand_uz="Oakley",
                rating=4.9, reviews_count=89, stock=20,
                variants=json.dumps([
                    {"size": "One Size", "color": "Matte Black", "colorHex": "#121212", "stock": 20}
                ]),
                shop_id=shop.id
            ),
             Product(
                name_ru="Prada Symbole",
                name_en="Prada Symbole",
                name_uz="Prada Symbole",
                description_ru="Геометрический дизайн с дерзким видом. Роскошные очки высочайшего качества.",
                description_en="Geometric design with a bold look. Luxury eyewear of the highest quality.",
                description_uz="Jasur ko'rinishga ega geometrik dizayn. Eng yuqori sifatli lyuks ko'zoynaklar.",
                price=450.00,
                image_url="https://images.unsplash.com/photo-1572635196237-14b3f281503f?q=80&w=2080&auto=format&fit=crop",
                images=json.dumps([
                    "https://images.unsplash.com/photo-1572635196237-14b3f281503f?q=80&w=2080&auto=format&fit=crop",
                    "https://images.unsplash.com/photo-1511499767150-a48a237f0083?q=80&w=2080&auto=format&fit=crop"
                ]),
                category_ru="Люксовые очки", category_en="Luxury Eyewear", category_uz="Lyuks ko'zoynaklar",
                brand_ru="Prada", brand_en="Prada", brand_uz="Prada",
                rating=5.0, reviews_count=32, stock=5,
                 variants=json.dumps([
                    {"size": "M", "color": "Black", "colorHex": "#000000", "stock": 5}
                ]),
                shop_id=shop.id
            ),
        ]
        session.add_all(products)
        session.commit()
        print("✓ Products created (multilingual)")
        
        # 7. Create banner
        banner = Banner(
            badge_text="NEW ARRIVAL",
            
            title="Ray-Ban Meta Smart Glasses",
            title_ru="Умные очки Ray-Ban Meta",
            title_en="Ray-Ban Meta Smart Glasses",
            title_uz="Ray-Ban Meta aqlli ko'zoynaklari",
            
            subtitle="The future of eyewear starting at $299",
            subtitle_ru="Будущее очков по цене от $299",
            subtitle_en="The future of eyewear starting at $299",
            subtitle_uz="Ko'zoynaklarning kelajagi $299 dan boshlanadi",
            
            button_text="Shop Collection",
            button_text_ru="Смотреть коллекцию",
            button_text_en="Shop Collection",
            button_text_uz="To'plamni ko'rish",
            
            button_link="/products",
            image_url="https://images.unsplash.com/photo-1572635196237-14b3f281503f?q=80&w=1200&auto=format&fit=crop",
            is_active=True,
            shop_id=shop.id
        )
        session.add(banner)
        session.commit()
        print("✓ Banner created")
        
        # 8. Create regular user
        regular_user = User(
            phone="998907654321",
            password_hash=get_password_hash("user123"),
            first_name="Maria",
            last_name="Ivanova",
            role="user"
        )
        session.add(regular_user)
        session.commit()
        print("✓ Regular user created: 998907654321 / user123")
        
        # 9. Create subscription plans
        plans = [
             SubscriptionPlan(
                name="Basic",
                slug="basic",
                price=29.99,
                period_days=30,
                description="For small shops",
                features=json.dumps(["Up to 50 products", "Basic analytics"]),
                is_active=True,
                is_trial=False,
                display_order=1
            ),
            SubscriptionPlan(
                name="Pro",
                slug="pro",
                price=79.99,
                period_days=30,
                description="For growing businesses",
                features=json.dumps(["Unlimited products", "Advanced analytics", "Priority support"]),
                is_active=True,
                is_trial=False,
                display_order=2
            ),
        ]
        session.add_all(plans)
        session.commit()
        print("✓ Subscription plans created")
        
        print("\nSUCCESS! Test data initialized.")

if __name__ == "__main__":
    clear_database()
    create_tables()
    init_test_data()
