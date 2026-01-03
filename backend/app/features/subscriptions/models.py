from sqlalchemy import Column, Integer, String, Float, Boolean, DateTime, ForeignKey
from datetime import datetime
from app.db.base_class import Base

class SubscriptionPlan(Base):
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    slug = Column(String, unique=True, index=True, nullable=False)
    price = Column(Float, nullable=False)
    period_days = Column(Integer, default=30)
    description = Column(String, nullable=True)
    features = Column(String, nullable=True) # JSON string
    is_active = Column(Boolean, default=True)
    is_trial = Column(Boolean, default=False)
    display_order = Column(Integer, default=0)
    max_products = Column(Integer, nullable=True)
    max_banners = Column(Integer, default=1)
    created_at = Column(DateTime, default=datetime.utcnow)

class SubscriptionRequest(Base):
    id = Column(Integer, primary_key=True, index=True)
    shop_id = Column(Integer, ForeignKey("shop.id"), index=True, nullable=False)
    plan_id = Column(Integer, ForeignKey("subscriptionplan.id"), nullable=False)
    duration_months = Column(Integer, default=1)
    type = Column(String, default="new") # new, renew, change
    status = Column(String, default="pending")
    requested_at = Column(DateTime, default=datetime.utcnow)
    approved_at = Column(DateTime, nullable=True)
    notes = Column(String, nullable=True)
