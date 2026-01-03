from fastapi import APIRouter, Depends, Query, HTTPException
from sqlalchemy.orm import Session
from typing import List, Optional
from app.db.session import get_db
from app.core.dependencies import get_current_user, get_current_platform_admin
from .service import SubscriptionService
from .schemas import (
    SubscriptionPlanRead, SubscriptionPlanCreate, SubscriptionPlanUpdate,
    SubscriptionRequestRead, SubscriptionRequestCreate, SubscriptionRequestUpdate
)

router = APIRouter()
subscription_service = SubscriptionService()

@router.get("/subscription-plans", response_model=List[SubscriptionPlanRead])
def get_plans(
    db: Session = Depends(get_db),
    active_only: bool = True
):
    """Get all subscription plans"""
    return subscription_service.get_plans(db, active_only)

@router.get("/platform/admin/subscription-plans", response_model=List[SubscriptionPlanRead])
def get_admin_plans(
    db: Session = Depends(get_db),
    admin = Depends(get_current_platform_admin)
):
    """Get all subscription plans (including inactive) - platform admin only"""
    return subscription_service.get_plans(db, active_only=False)

@router.post("/platform/admin/subscription-plans", response_model=SubscriptionPlanRead)
def create_plan(
    plan_in: SubscriptionPlanCreate,
    db: Session = Depends(get_db),
    admin = Depends(get_current_platform_admin)
):
    """Create a subscription plan - platform admin only"""
    return subscription_service.create_plan(db, plan_in)

@router.put("/platform/admin/subscription-plans/{plan_id}", response_model=SubscriptionPlanRead)
def update_plan(
    plan_id: int,
    plan_in: SubscriptionPlanUpdate,
    db: Session = Depends(get_db),
    admin = Depends(get_current_platform_admin)
):
    """Update a subscription plan - platform admin only"""
    return subscription_service.update_plan(db, plan_id, plan_in)

@router.delete("/platform/admin/subscription-plans/{plan_id}", response_model=SubscriptionPlanRead)
def delete_plan(
    plan_id: int,
    db: Session = Depends(get_db),
    admin = Depends(get_current_platform_admin)
):
    """Delete a subscription plan - platform admin only"""
    return subscription_service.delete_plan(db, plan_id)

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
    shop_id: Optional[int] = Query(None),
    db: Session = Depends(get_db),
    current_user = Depends(get_current_platform_admin)
):
    """Get all subscription requests - platform admin only"""
    return subscription_service.get_all_requests(db, status, shop_id)

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
@router.post("/subscription-requests", response_model=SubscriptionRequestRead)
def create_subscription_request(
    request_in: SubscriptionRequestCreate,
    shop_slug: str = Query(..., description="Shop Slug"),
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """Create a subscription request (new/renew/change) - Shop Owner"""
    return subscription_service.create_subscription_request(db, shop_slug, request_in, current_user)

@router.get("/subscription-requests/my", response_model=Optional[SubscriptionRequestRead])
def get_my_subscription_request(
    shop_slug: str = Query(..., description="Shop Slug"),
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """Get active subscription request for a shop - Shop Owner"""
    return subscription_service.get_shop_subscription_request(db, shop_slug, current_user)

@router.get("/platform/admin/subscription-requests", response_model=List[SubscriptionRequestRead])
def get_all_requests(
    status: Optional[str] = None,
    shop_id: Optional[int] = None,
    db: Session = Depends(get_db),
    admin = Depends(get_current_platform_admin)
):
    """Get all subscription requests - Platform Admin"""
    return subscription_service.get_all_requests(db, status, shop_id)

@router.put("/platform/admin/subscription-requests/{request_id}/status", response_model=SubscriptionRequestRead)
def update_request_status(
    request_id: int,
    update_in: SubscriptionRequestUpdate,
    db: Session = Depends(get_db),
    admin = Depends(get_current_platform_admin)
):
    """Approve or reject subscription request"""
    return subscription_service.update_request_status(db, request_id, update_in)

@router.post("/subscription/cancel")
def cancel_subscription(
    shop_slug: str = Query(..., description="Shop Slug"),
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """Cancel subscription - Shop Owner"""
    return subscription_service.cancel_subscription(db, shop_slug, current_user)
