from app.db.session import SessionLocal
from app.features.subscriptions.models import SubscriptionPlan
from sqlalchemy import text

def update_plans():
    db = SessionLocal()
    try:
        # Update or create plans
        # Plan 1: Trial
        trial = db.query(SubscriptionPlan).filter(SubscriptionPlan.slug == "trial").first()
        if trial:
            trial.can_broadcast = False
        
        # Plan 2: Business (renamed from Basic if exists, or create)
        business = db.query(SubscriptionPlan).filter(SubscriptionPlan.slug == "business").first()
        if not business:
            # Check if basic exists and rename it
            basic = db.query(SubscriptionPlan).filter(SubscriptionPlan.slug == "basic").first()
            if basic:
                basic.name = "Бизнес"
                basic.slug = "business"
                basic.description = "Идеально для растущих магазинов с рассылками"
                basic.features = "До 200 товаров,Рассылки в Telegram (до 500/мес),Приоритетная поддержка"
                basic.can_broadcast = True
            else:
                business = SubscriptionPlan(
                    name="Бизнес",
                    slug="business",
                    price=29.0,
                    period_days=30,
                    description="Идеально для растущих магазинов с рассылками",
                    features="До 200 товаров,Рассылки в Telegram (до 500/мес),Приоритетная поддержка",
                    can_broadcast=True,
                    display_order=2
                )
                db.add(business)
        else:
            business.can_broadcast = True
            business.name = "Бизнес"

        # Plan 3: Premium
        premium = db.query(SubscriptionPlan).filter(SubscriptionPlan.slug == "premium").first()
        if premium:
            premium.can_broadcast = True
            premium.description = "Безлимитные возможности для вашего бренда"
            premium.features = "Безлимитные товары,Безлимитные рассылки,Подробная статистика,Личный менеджер"
        
        db.commit()
        print("Subscription plans updated successfully!")
    except Exception as e:
        print(f"Error updating plans: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    update_plans()
