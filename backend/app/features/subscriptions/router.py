from fastapi import APIRouter, Depends, Query, HTTPException
from sqlalchemy.orm import Session
from typing import List, Optional
from app.db.session import get_db
from app.core.dependencies import get_current_user, get_current_platform_admin
from .service import SubscriptionService
from .schemas import SubscriptionPlanRead, SubscriptionRequestRead, SubscriptionRequestCreate, SubscriptionRequestUpdate

router = APIRouter()
subscription_service = SubscriptionService()

@router.get("/subscription-plans", response_model=List[SubscriptionPlanRead])
def get_plans(db: Session = Depends(get_db)):
    """Get all active subscription plans"""
    return subscription_service.get_plans(db)

@router.post("/shop/{shop_slug}/subscription/request", response_model=SubscriptionRequestRead)
def create_subscription_request(
    shop_slug: str,
    request_in: SubscriptionRequestCreate,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """Create a subscription request - shop owner only"""
    return subscription_service.create_subscription_request(db, shop_slug, request_in, current_user)

@router.get("/shop/{shop_slug}/subscription/request", response_model=Optional[SubscriptionRequestRead])
def get_shop_subscription_request(
    shop_slug: str,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """Get current subscription request for shop - shop owner only"""
    return subscription_service.get_shop_subscription_request(db, shop_slug, current_user)

@router.get("/platform/admin/subscription-requests", response_model=List[SubscriptionRequestRead])
def get_all_subscription_requests(
    status: Optional[str] = Query(None),
    db: Session = Depends(get_db),
    current_user = Depends(get_current_platform_admin)
):
    """Get all subscription requests - platform admin only"""
    return subscription_service.get_all_requests(db, status)

@router.put("/platform/admin/subscription-requests/{request_id}", response_model=SubscriptionRequestRead)
def update_subscription_request(
    request_id: int,
    update_in: SubscriptionRequestUpdate,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_platform_admin)
):
    """Approve or reject subscription request - platform admin only"""
    return subscription_service.update_request_status(db, request_id, update_in)

@router.post("/shop/{shop_slug}/subscription/cancel")
def cancel_subscription(
    shop_slug: str,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """Cancel subscription - shop owner only"""
    return subscription_service.cancel_subscription(db, shop_slug, current_user)
