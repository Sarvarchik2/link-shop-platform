
import os
import sys
import random
from datetime import datetime, timedelta

# Add backend directory to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from sqlalchemy.orm import Session
from app.db.session import SessionLocal, engine
from app.db.base_class import Base

# Import Models
from app.features.users.models import User
from app.features.shops.models import Shop
from app.features.products.models import Product
from app.features.categories.models import Category
from app.features.brands.models import Brand
from app.features.orders.models import Order, OrderItem
from app.features.subscriptions.models import SubscriptionPlan
from app.features.banners.models import Banner
from app.features.offers.models import Offer
from app.core.security import get_password_hash

def reseed_database():
    print("🗑️  Wiping database...")
    Base.metadata.drop_all(bind=engine)
    print("✨ Creating fresh schema...")
    Base.metadata.create_all(bind=engine)

    db = SessionLocal()
    try:
        # 1. Create Subscription Plans
        print("📦 Seeding Subscription Plans...")
        plans = [
            SubscriptionPlan(id=1, name="Пробный период", slug="trial", price=0.0, period_days=30, is_trial=True, max_products=50, features="Базовая аналитика,До 50 товаров"),
            SubscriptionPlan(id=2, name="Базовый", slug="basic", price=29.0, period_days=30, max_products=200, features="Расширенная аналитика,До 200 товаров,Приоритетная поддержка"),
            SubscriptionPlan(id=3, name="Премиум", slug="premium", price=79.0, period_days=30, max_products=10000, features="Безлимит товаров,Личный менеджер,API доступ")
        ]
        db.add_all(plans)
        db.commit()

        # 2. Create Users
        print("👥 Seeding Users...")
        # Platform Admin
        admin = User(
            phone="+998900000000",
            password_hash=get_password_hash("admin123"),
            first_name="Platform",
            last_name="Admin",
            role="platform_admin"
        )
        
        # Fashion Owner (Premium)
        fashion_owner = User(
            phone="+998901111111",
            password_hash=get_password_hash("password123"),
            first_name="Anna",
            last_name="Style",
            role="shop_owner"
        )

        # Tech Owner (Basic)
        tech_owner = User(
            phone="+998902222222",
            password_hash=get_password_hash("password123"),
            first_name="Mike",
            last_name="Geek",
            role="shop_owner"
        )

        # Trial Owner
        trial_owner = User(
            phone="+998903333333",
            password_hash=get_password_hash("password123"),
            first_name="John",
            last_name="Doe",
            role="shop_owner"
        )
        
        # Customer
        customer = User(
            phone="+998904444444",
            password_hash=get_password_hash("password123"),
            first_name="Client",
            last_name="One",
            role="user"
        )

        db.add_all([admin, fashion_owner, tech_owner, trial_owner, customer])
        db.commit()

        # 3. Create Shops
        print("🏪 Seeding Shops...")
        
        # Style Haven (Fashion)
        style_haven = Shop(
            name="Style Haven",
            slug="style-haven",
            owner_id=fashion_owner.id,
            description="Leading fashion destination for modern trends.",
            subscription_status="active",
            subscription_plan_id=3, # Premium
            subscription_expires_at=datetime.utcnow() + timedelta(days=25),
            is_active=True,
            phone="+998901111111",
            email="contact@stylehaven.com"
        )

        # Gizmo World (Tech)
        gizmo_world = Shop(
            name="Gizmo World",
            slug="gizmo-world",
            owner_id=tech_owner.id,
            description="Best gadgets and electronics in town.",
            subscription_status="active",
            subscription_plan_id=2, # Basic
            subscription_expires_at=datetime.utcnow() + timedelta(days=15),
            is_active=True,
            phone="+998902222222",
            email="support@gizmo.com"
        )
        
        # Newbie Store (Trial)
        newbie_store = Shop(
            name="Newbie Store",
            slug="newbie-store",
            owner_id=trial_owner.id,
            description="Just getting started.",
            subscription_status="trial",
            subscription_plan_id=1, # Trial
            subscription_expires_at=datetime.utcnow() + timedelta(days=29),
            is_active=True
        )

        db.add_all([style_haven, gizmo_world, newbie_store])
        db.commit()

        # 4. Seed Data: Fashion Shop
        print("👗 Seeding Fashion Data...")
        
        # Categories
        cat_men = Category(name="Men", shop_id=style_haven.id)
        cat_women = Category(name="Women", shop_id=style_haven.id)
        cat_acc = Category(name="Accessories", shop_id=style_haven.id)
        db.add_all([cat_men, cat_women, cat_acc])
        db.commit()

        # Brands
        brand_nike = Brand(name="Nike", shop_id=style_haven.id, logo_url="")
        brand_zara = Brand(name="Zara", shop_id=style_haven.id, logo_url="")
        brand_gucci = Brand(name="Gucci", shop_id=style_haven.id, logo_url="")
        db.add_all([brand_nike, brand_zara, brand_gucci])
        db.commit()

        # Products (20 items)
        fashion_products = []
        for i in range(10):
            p = Product(
                name=f"Premium T-Shirt {i+1}",
                description="High quality cotton t-shirt with modern fit.",
                price=25.0 + i,
                image_url="https://images.unsplash.com/photo-1521572163474-6864f9cf17ab?auto=format&fit=crop&w=500&q=80",
                category=cat_men.name if i % 2 == 0 else cat_women.name,
                brand=brand_nike.name if i % 2 == 0 else brand_zara.name,
                stock=100,
                shop_id=style_haven.id,
                is_preorder_enabled=False
            )
            fashion_products.append(p)
        
        for i in range(10):
             p = Product(
                name=f"Designer Jacket {i+1}",
                description="Winter collection jacket.",
                price=120.0 + (i*5),
                image_url="https://images.unsplash.com/photo-1551028919-ac66e6246958?auto=format&fit=crop&w=500&q=80",
                category=cat_women.name,
                brand=brand_gucci.name,
                stock=50,
                shop_id=style_haven.id,
                is_preorder_enabled=False
            )
             fashion_products.append(p)

        db.add_all(fashion_products)
        db.commit()

        # Orders (50 mixed)
        statuses = ["pending", "processing", "shipping", "delivered", "cancelled"]
        for i in range(50):
            status = random.choice(statuses)
            # Create order
            order_date = datetime.utcnow() - timedelta(days=random.randint(0, 60))
            
            # Select random products
            items_count = random.randint(1, 3)
            selected_products = random.sample(fashion_products, items_count)
            total_price = sum(p.price for p in selected_products)

            order = Order(
                shop_id=style_haven.id,
                user_id=customer.id, # All from same customer for simplicity or leave null if guest allowed (but model says user_id foreign key)
                status=status,
                total_price=total_price,
                recipient_name=f"Customer {i}",
                delivery_phone="+998901234567",
                delivery_address="Tashkent City",
                created_at=order_date
            )
            db.add(order)
            db.commit() # Commit to get ID

            for p in selected_products:
                item = OrderItem(
                    order_id=order.id,
                    product_id=p.id,
                    quantity=1,
                    price=p.price
                )
                db.add(item)
            db.commit()

        # 5. Seed Data: Tech Shop
        print("📱 Seeding Tech Data...")
        
        # Categories
        cat_phones = Category(name="Phones", shop_id=gizmo_world.id)
        cat_laptops = Category(name="Laptops", shop_id=gizmo_world.id)
        db.add_all([cat_phones, cat_laptops])
        db.commit()

        # Brands
        brand_apple = Brand(name="Apple", shop_id=gizmo_world.id, logo_url="")
        brand_samsung = Brand(name="Samsung", shop_id=gizmo_world.id, logo_url="")
        db.add_all([brand_apple, brand_samsung])
        db.commit()

        # Products
        tech_products = []
        tech_items = [
            ("iPhone 15 Pro", 999.0, cat_phones, brand_apple, "https://images.unsplash.com/photo-1695048133142-1a20484d2569?auto=format&fit=crop&w=500&q=80"),
            ("Samsung S24 Ultra", 1199.0, cat_phones, brand_samsung, "https://images.unsplash.com/photo-1610945415295-d9bbf067e59c?auto=format&fit=crop&w=500&q=80"),
            ("MacBook Pro 14", 1999.0, cat_laptops, brand_apple, "https://images.unsplash.com/photo-1517336714731-489689fd1ca4?auto=format&fit=crop&w=500&q=80"),
            ("Samsung Galaxy Book", 1499.0, cat_laptops, brand_samsung, "https://images.unsplash.com/photo-1531297461136-82lw8a1599b?auto=format&fit=crop&w=500&q=80"),
        ]
        
        for name, price, cat, brand, img in tech_items:
            p = Product(
                name=name,
                description=f"Latest flagship {name}.",
                price=price,
                image_url=img,
                category=cat.name,
                brand=brand.name,
                stock=20,
                shop_id=gizmo_world.id
            )
            tech_products.append(p)
        db.add_all(tech_products)
        db.commit()

        # Orders (10 orders)
        for i in range(10):
            order = Order(
                shop_id=gizmo_world.id,
                user_id=customer.id,
                status="delivered",
                total_price=random.choice(tech_items)[1],
                recipient_name="Tech Buyer",
                delivery_phone="+998909999999",
                delivery_address="Cyber City",
                created_at=datetime.utcnow() - timedelta(days=i)
            )
            db.add(order)
        db.commit()

        print("✅ Database reseed complete!")

    except Exception as e:
        print(f"❌ Error seeding database: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    reseed_database()
