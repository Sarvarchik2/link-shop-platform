
import sys
import os

# Add backend directory to path
sys.path.append(os.path.join(os.getcwd(), 'backend'))

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.core.config import settings
from app.features.subscriptions.models import SubscriptionPlan

# Setup DB connection
engine = create_engine(settings.DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
db = SessionLocal()

try:
    plans = db.query(SubscriptionPlan).all()
    print(f"Found {len(plans)} plans:")
    for p in plans:
        print(f"- ID: {p.id}, Name: {p.name}, Slug: {p.slug}, Price: {p.price}, Period: {p.period_days} days, Is Trial: {p.is_trial}")
except Exception as e:
    print(f"Error: {e}")
finally:
    db.close()
