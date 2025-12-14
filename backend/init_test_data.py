#!/usr/bin/env python3
"""
Скрипт для очистки базы данных и создания тестовых данных:
- Владелец магазина с полностью оформленным магазином
- Обычный пользователь
- Платформенный админ
"""

import os
import json
from datetime import datetime, timedelta
from sqlmodel import Session, SQLModel, create_engine, select
from main import (
    User, Shop, Product, Brand, Category, Banner, SubscriptionPlan,
    get_password_hash
)

# Database setup
sqlite_file_name = "database.db"
sqlite_url = f"sqlite:///{sqlite_file_name}"
connect_args = {"check_same_thread": False}
engine = create_engine(sqlite_url, echo=False, connect_args=connect_args)

def clear_database():
    """Удаляет базу данных если она существует"""
    if os.path.exists(sqlite_file_name):
        os.remove(sqlite_file_name)
        print("✓ База данных удалена")
    else:
        print("✓ База данных не существует, создаем новую")

def create_tables():
    """Создает все таблицы"""
    SQLModel.metadata.create_all(engine)
    print("✓ Таблицы созданы")

def init_test_data():
    """Создает тестовые данные"""
    with Session(engine) as session:
        # 1. Создаем платформенного админа
        admin = User(
            phone="admin",
            password_hash=get_password_hash("admin123"),
            first_name="Admin",
            last_name="System",
            role="platform_admin"
        )
        session.add(admin)
        session.commit()
        session.refresh(admin)
        print("✓ Платформенный админ создан: admin / admin123")
        
        # 2. Создаем владельца магазина
        shop_owner = User(
            phone="shopowner",
            password_hash=get_password_hash("owner123"),
            first_name="Иван",
            last_name="Петров",
            role="shop_owner"
        )
        session.add(shop_owner)
        session.commit()
        session.refresh(shop_owner)
        print("✓ Владелец магазина создан: shopowner / owner123")
        
        # 3. Создаем магазин
        subscription_expires = datetime.utcnow() + timedelta(days=365)
        shop = Shop(
            name="Premium Eyewear Store",
            slug="premium-eyewear",
            owner_id=shop_owner.id,
            description="Премиальный магазин очков и солнцезащитных очков. Широкий ассортимент брендовых моделей от ведущих производителей.",
            logo_url="https://images.unsplash.com/photo-1572635196237-14b3f281503f?q=80&w=200&auto=format&fit=crop",
            subscription_status="active",
            subscription_expires_at=subscription_expires,
            is_active=True
        )
        session.add(shop)
        session.commit()
        session.refresh(shop)
        print("✓ Магазин создан: Premium Eyewear Store (slug: premium-eyewear)")
        
        # 4. Создаем бренды для магазина
        brands = [
            Brand(name="Ray-Ban", logo_url="https://upload.wikimedia.org/wikipedia/commons/thumb/0/03/Ray-Ban_logo.svg/2560px-Ray-Ban_logo.svg.png", shop_id=shop.id),
            Brand(name="Oakley", logo_url="https://upload.wikimedia.org/wikipedia/commons/thumb/f/f6/Oakley_logo.svg/2560px-Oakley_logo.svg.png", shop_id=shop.id),
            Brand(name="Prada", logo_url="https://upload.wikimedia.org/wikipedia/commons/thumb/b/b8/Prada-Logo.svg/2560px-Prada-Logo.svg.png", shop_id=shop.id),
            Brand(name="Gucci", logo_url="https://upload.wikimedia.org/wikipedia/commons/thumb/7/79/Gucci_Logo.svg/2560px-Gucci_Logo.svg.png", shop_id=shop.id),
            Brand(name="Tom Ford", logo_url="https://upload.wikimedia.org/wikipedia/commons/thumb/9/9a/Tom_Ford_logo.svg/2560px-Tom_Ford_logo.svg.png", shop_id=shop.id),
        ]
        for brand in brands:
            session.add(brand)
        session.commit()
        print("✓ Бренды созданы (5 шт)")
        
        # 5. Создаем категории для магазина
        categories = [
            Category(name="Солнцезащитные очки", image_url="https://images.unsplash.com/photo-1511499767150-a48a237f0083?q=80&w=2080&auto=format&fit=crop", shop_id=shop.id),
            Category(name="Умные очки", image_url="https://images.unsplash.com/photo-1572635196237-14b3f281503f?q=80&w=2080&auto=format&fit=crop", shop_id=shop.id),
            Category(name="Очки для зрения", image_url="https://images.unsplash.com/photo-1577803645773-f96470509666?q=80&w=2080&auto=format&fit=crop", shop_id=shop.id),
            Category(name="Люксовые очки", image_url="https://images.unsplash.com/photo-1511499767150-a48a237f0083?q=80&w=2080&auto=format&fit=crop", shop_id=shop.id),
            Category(name="Спортивные очки", image_url="https://images.unsplash.com/photo-1572635196237-14b3f281503f?q=80&w=2080&auto=format&fit=crop", shop_id=shop.id),
        ]
        for category in categories:
            session.add(category)
        session.commit()
        print("✓ Категории созданы (5 шт)")
        
        # 6. Создаем товары для магазина
        products = [
            Product(
                name="Ray-Ban Meta Wayfarer",
                description="Классический стиль Wayfarer с умными функциями. Встроенная камера и динамики для максимального опыта использования умных очков.",
                price=299.00,
                image_url="https://images.unsplash.com/photo-1572635196237-14b3f281503f?q=80&w=2080&auto=format&fit=crop",
                images=json.dumps([
                    "https://images.unsplash.com/photo-1572635196237-14b3f281503f?q=80&w=2080&auto=format&fit=crop",
                    "https://images.unsplash.com/photo-1511499767150-a48a237f0083?q=80&w=2080&auto=format&fit=crop",
                    "https://images.unsplash.com/photo-1577803645773-f96470509666?q=80&w=2080&auto=format&fit=crop"
                ]),
                category="Умные очки",
                brand="Ray-Ban",
                rating=4.5,
                reviews_count=120,
                stock=15,
                variants=json.dumps([
                    {"size": "S", "color": "Черный", "colorHex": "#000000", "stock": 5},
                    {"size": "M", "color": "Черный", "colorHex": "#000000", "stock": 3},
                    {"size": "L", "color": "Черный", "colorHex": "#000000", "stock": 2},
                    {"size": "M", "color": "Черепаховый", "colorHex": "#8B4513", "stock": 3},
                    {"size": "L", "color": "Черепаховый", "colorHex": "#8B4513", "stock": 2},
                ]),
                shop_id=shop.id
            ),
            Product(
                name="Ray-Ban Aviator Classic",
                description="Легендарный стиль, с которого все началось. Классический дизайн авиатора.",
                price=163.00,
                image_url="https://images.unsplash.com/photo-1572635196237-14b3f281503f?q=80&w=2080&auto=format&fit=crop",
                images=json.dumps([
                    "https://images.unsplash.com/photo-1572635196237-14b3f281503f?q=80&w=2080&auto=format&fit=crop",
                    "https://images.unsplash.com/photo-1577803645773-f96470509666?q=80&w=2080&auto=format&fit=crop"
                ]),
                category="Солнцезащитные очки",
                brand="Ray-Ban",
                rating=4.6,
                reviews_count=200,
                stock=30,
                variants=json.dumps([
                    {"size": "S", "color": "Золото/Зеленый", "colorHex": "#FFD700", "stock": 10},
                    {"size": "M", "color": "Золото/Зеленый", "colorHex": "#FFD700", "stock": 5},
                    {"size": "S", "color": "Серебро/Синий", "colorHex": "#C0C0C0", "stock": 8},
                    {"size": "M", "color": "Серебро/Синий", "colorHex": "#C0C0C0", "stock": 5},
                    {"size": "L", "color": "Черный", "colorHex": "#000000", "stock": 2},
                ]),
                shop_id=shop.id
            ),
            Product(
                name="Oakley Holbrook",
                description="Вневременной классический дизайн в сочетании с современными технологиями Oakley. Прочные и стильные.",
                price=150.00,
                image_url="https://images.unsplash.com/photo-1577803645773-f96470509666?q=80&w=2080&auto=format&fit=crop",
                images=json.dumps([
                    "https://images.unsplash.com/photo-1577803645773-f96470509666?q=80&w=2080&auto=format&fit=crop"
                ]),
                category="Солнцезащитные очки",
                brand="Oakley",
                rating=4.8,
                reviews_count=210,
                stock=25,
                variants=json.dumps([
                    {"size": "S", "color": "Матовый черный", "colorHex": "#1a1a1a", "stock": 5},
                    {"size": "M", "color": "Матовый черный", "colorHex": "#1a1a1a", "stock": 5},
                    {"size": "L", "color": "Полированный черный", "colorHex": "#000000", "stock": 8},
                    {"size": "XL", "color": "Полированный черный", "colorHex": "#000000", "stock": 4},
                    {"size": "M", "color": "Коричневый черепаховый", "colorHex": "#654321", "stock": 3},
                ]),
                shop_id=shop.id
            ),
            Product(
                name="Prada Symbole",
                description="Геометрический дизайн с дерзким видом. Роскошные очки высочайшего качества.",
                price=450.00,
                image_url="https://images.unsplash.com/photo-1572635196237-14b3f281503f?q=80&w=2080&auto=format&fit=crop",
                images=json.dumps([
                    "https://images.unsplash.com/photo-1572635196237-14b3f281503f?q=80&w=2080&auto=format&fit=crop",
                    "https://images.unsplash.com/photo-1511499767150-a48a237f0083?q=80&w=2080&auto=format&fit=crop"
                ]),
                category="Люксовые очки",
                brand="Prada",
                rating=4.9,
                reviews_count=45,
                stock=12,
                variants=json.dumps([
                    {"size": "M", "color": "Черный", "colorHex": "#000000", "stock": 6},
                    {"size": "L", "color": "Черный", "colorHex": "#000000", "stock": 3},
                    {"size": "M", "color": "Золото", "colorHex": "#FFD700", "stock": 2},
                    {"size": "L", "color": "Золото", "colorHex": "#FFD700", "stock": 1},
                ]),
                shop_id=shop.id
            ),
            Product(
                name="Gucci GG0061S",
                description="Круглые металлические солнцезащитные очки с винтажным оттенком. Знаковый стиль Gucci.",
                price=380.00,
                image_url="https://images.unsplash.com/photo-1511499767150-a48a237f0083?q=80&w=2080&auto=format&fit=crop",
                images=json.dumps([
                    "https://images.unsplash.com/photo-1511499767150-a48a237f0083?q=80&w=2080&auto=format&fit=crop"
                ]),
                category="Люксовые очки",
                brand="Gucci",
                rating=4.6,
                reviews_count=60,
                stock=12,
                variants=json.dumps([
                    {"size": "S", "color": "Золото", "colorHex": "#FFD700", "stock": 3},
                    {"size": "M", "color": "Золото", "colorHex": "#FFD700", "stock": 3},
                    {"size": "S", "color": "Серебро", "colorHex": "#C0C0C0", "stock": 3},
                    {"size": "M", "color": "Серебро", "colorHex": "#C0C0C0", "stock": 3},
                ]),
                shop_id=shop.id
            ),
            Product(
                name="Tom Ford FT5400",
                description="Элегантные прямоугольные очки с золотыми акцентами. Премиальное качество и стиль.",
                price=420.00,
                image_url="https://images.unsplash.com/photo-1572635196237-14b3f281503f?q=80&w=2080&auto=format&fit=crop",
                images=json.dumps([
                    "https://images.unsplash.com/photo-1572635196237-14b3f281503f?q=80&w=2080&auto=format&fit=crop",
                    "https://images.unsplash.com/photo-1511499767150-a48a237f0083?q=80&w=2080&auto=format&fit=crop"
                ]),
                category="Люксовые очки",
                brand="Tom Ford",
                rating=4.7,
                reviews_count=88,
                stock=18,
                variants=json.dumps([
                    {"size": "M", "color": "Черный", "colorHex": "#000000", "stock": 6},
                    {"size": "L", "color": "Черный", "colorHex": "#000000", "stock": 4},
                    {"size": "M", "color": "Коричневый", "colorHex": "#8B4513", "stock": 5},
                    {"size": "L", "color": "Коричневый", "colorHex": "#8B4513", "stock": 3},
                ]),
                shop_id=shop.id
            ),
            Product(
                name="Ray-Ban Meta Headliner",
                description="Круглая форма для ретро-образа. Идеально подходит для повседневной носки с передовой аудиотехнологией.",
                price=329.00,
                image_url="https://images.unsplash.com/photo-1511499767150-a48a237f0083?q=80&w=2080&auto=format&fit=crop",
                images=json.dumps([
                    "https://images.unsplash.com/photo-1511499767150-a48a237f0083?q=80&w=2080&auto=format&fit=crop",
                    "https://images.unsplash.com/photo-1572635196237-14b3f281503f?q=80&w=2080&auto=format&fit=crop"
                ]),
                category="Умные очки",
                brand="Ray-Ban",
                rating=4.7,
                reviews_count=85,
                stock=8,
                variants=json.dumps([
                    {"size": "M", "color": "Матовый черный", "colorHex": "#1a1a1a", "stock": 3},
                    {"size": "L", "color": "Матовый черный", "colorHex": "#1a1a1a", "stock": 2},
                    {"size": "M", "color": "Блестящий черный", "colorHex": "#000000", "stock": 2},
                    {"size": "L", "color": "Блестящий черный", "colorHex": "#000000", "stock": 1},
                ]),
                shop_id=shop.id
            ),
            Product(
                name="Oakley Radar EV",
                description="Спортивные очки с защитой от ультрафиолета и превосходной оптикой. Для активного образа жизни.",
                price=180.00,
                image_url="https://images.unsplash.com/photo-1577803645773-f96470509666?q=80&w=2080&auto=format&fit=crop",
                images=json.dumps([
                    "https://images.unsplash.com/photo-1577803645773-f96470509666?q=80&w=2080&auto=format&fit=crop"
                ]),
                category="Спортивные очки",
                brand="Oakley",
                rating=4.5,
                reviews_count=150,
                stock=20,
                variants=json.dumps([
                    {"size": "M", "color": "Черный", "colorHex": "#000000", "stock": 8},
                    {"size": "L", "color": "Черный", "colorHex": "#000000", "stock": 6},
                    {"size": "M", "color": "Синий", "colorHex": "#1E40AF", "stock": 4},
                    {"size": "L", "color": "Синий", "colorHex": "#1E40AF", "stock": 2},
                ]),
                shop_id=shop.id
            ),
        ]
        
        for product in products:
            session.add(product)
        session.commit()
        print("✓ Товары созданы (8 шт)")
        
        # 7. Создаем баннер для магазина
        banner = Banner(
            badge_text="НОВИНКА",
            title="Ray-Ban Meta Smart Glasses",
            subtitle="От $299",
            button_text="Купить сейчас",
            button_link="/products",
            image_url="https://images.unsplash.com/photo-1572635196237-14b3f281503f?q=80&w=800&auto=format&fit=crop",
            is_active=True,
            shop_id=shop.id
        )
        session.add(banner)
        session.commit()
        print("✓ Баннер создан")
        
        # 8. Создаем обычного пользователя
        regular_user = User(
            phone="user123",
            password_hash=get_password_hash("user123"),
            first_name="Мария",
            last_name="Иванова",
            role="user"
        )
        session.add(regular_user)
        session.commit()
        print("✓ Обычный пользователь создан: user123 / user123")
        
        # 9. Создаем планы подписки
        plans = [
            SubscriptionPlan(
                name="Базовый",
                slug="basic",
                price=29.99,
                period_days=30,
                description="Базовый план для начинающих продавцов",
                features=json.dumps(["До 50 товаров", "Базовая аналитика", "Email поддержка"]),
                is_active=True,
                is_trial=False,
                display_order=1
            ),
            SubscriptionPlan(
                name="Профессиональный",
                slug="pro",
                price=79.99,
                period_days=30,
                description="Для растущего бизнеса",
                features=json.dumps(["Неограниченное количество товаров", "Расширенная аналитика", "Приоритетная поддержка", "Кастомный домен"]),
                is_active=True,
                is_trial=False,
                display_order=2
            ),
            SubscriptionPlan(
                name="Премиум",
                slug="premium",
                price=149.99,
                period_days=30,
                description="Максимальные возможности",
                features=json.dumps(["Все функции Pro", "Персональный менеджер", "API доступ", "Белый лейбл"]),
                is_active=True,
                is_trial=False,
                display_order=3
            ),
        ]
        for plan in plans:
            session.add(plan)
        session.commit()
        print("✓ Планы подписки созданы (3 шт)")
        
        print("\n" + "="*60)
        print("ТЕСТОВЫЕ ДАННЫЕ СОЗДАНЫ УСПЕШНО!")
        print("="*60)
        print("\n📋 ДОСТУПЫ ДЛЯ ВХОДА:\n")
        print("1. ПЛАТФОРМЕННЫЙ АДМИН:")
        print("   Логин: admin")
        print("   Пароль: admin123")
        print("   URL: http://localhost:3000/platform/admin")
        print()
        print("2. ВЛАДЕЛЕЦ МАГАЗИНА:")
        print("   Логин: shopowner")
        print("   Пароль: owner123")
        print("   URL: http://localhost:3000/shop/premium-eyewear/admin")
        print()
        print("3. ОБЫЧНЫЙ ПОЛЬЗОВАТЕЛЬ:")
        print("   Логин: user123")
        print("   Пароль: user123")
        print("   URL: http://localhost:3000/login")
        print()
        print("="*60)
        print("Магазин: Premium Eyewear Store")
        print("Slug: premium-eyewear")
        print("Товаров: 8")
        print("Брендов: 5")
        print("Категорий: 5")
        print("="*60)

if __name__ == "__main__":
    print("Начинаю инициализацию тестовых данных...\n")
    clear_database()
    create_tables()
    init_test_data()
    print("\n✓ Готово! Можете тестировать приложение.")
