from app.db.session import SessionLocal
from app.features.subscriptions.models import SubscriptionRequest, SubscriptionPlan
from app.features.shops.models import Shop
from app.core.config import settings
import datetime

print(f"DB URL: {settings.DATABASE_URL}")

db = SessionLocal()
try:
    # Check Plan
    plan = db.query(SubscriptionPlan).first()
    if not plan:
        print("No plans found!")
        exit()
    print(f"Using Plan: {plan.name} (ID: {plan.id})")

    # Check Shop
    shop = db.query(Shop).filter(Shop.slug == 'serik').first()
    if not shop:
        print("Shop 'serik' not found!")
        exit()
    print(f"Using Shop: {shop.name} (ID: {shop.id})")
    
    # Create Request
    print("Creating dummy request...")
    req = SubscriptionRequest(
        shop_id=shop.id,
        plan_id=plan.id,
        duration_months=1,
        status='pending',
        requested_at=datetime.datetime.utcnow()
    )
    db.add(req)
    db.commit()
    db.refresh(req)
    print(f"Created Request ID: {req.id}")

    # Verify
    count = db.query(SubscriptionRequest).count()
    print(f"New Request Count: {count}")
    
finally:
    db.close()
