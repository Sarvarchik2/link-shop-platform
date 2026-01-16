"""
Script to enable broadcasts for all active shops (for testing)
Run this on Railway to enable broadcasts for your shop
"""
from app.db.session import SessionLocal
from app.features.subscriptions.models import SubscriptionPlan
from app.features.shops.models import Shop
from sqlalchemy import text

def enable_broadcasts_for_all():
    db = SessionLocal()
    try:
        # Enable broadcasts for all plans (for testing/demo)
        plans = db.query(SubscriptionPlan).all()
        for plan in plans:
            plan.can_broadcast = True
            print(f"✓ Enabled broadcasts for plan: {plan.name}")
        
        db.commit()
        print("\n✅ All subscription plans now support broadcasts!")
        
        # Check current shops
        shops = db.query(Shop).all()
        for shop in shops:
            plan = db.query(SubscriptionPlan).filter(SubscriptionPlan.id == shop.subscription_plan_id).first()
            print(f"\nShop: {shop.name} ({shop.slug})")
            print(f"  Plan: {plan.name if plan else 'No plan'}")
            print(f"  Can broadcast: {plan.can_broadcast if plan else 'N/A'}")
            
    except Exception as e:
        print(f"❌ Error: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    enable_broadcasts_for_all()
