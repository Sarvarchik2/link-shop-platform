from fastapi import APIRouter, Depends, Query, HTTPException
from sqlalchemy.orm import Session
from typing import List, Optional
from app.db.session import get_db
from .service import OrderService
from .schemas import OrderCreate, OrderRead, OrderReadWithItems, OrderStatusUpdate
from app.core.dependencies import get_current_user, get_current_platform_admin
from app.features.subscriptions.dependencies import check_shop_active

router = APIRouter()
order_service = OrderService()

@router.post("/orders", response_model=OrderRead)
def create_order(
    order_in: OrderCreate,
    shop_slug: Optional[str] = Query(None),
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    return order_service.create_order(db, order_in, current_user.id, shop_slug)

@router.get("/orders/me", response_model=List[OrderReadWithItems])
def get_my_orders_alt(
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    return order_service.get_user_orders(db, current_user.id)

@router.get("/orders", response_model=List[OrderReadWithItems])
def get_my_orders(
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    return order_service.get_user_orders(db, current_user.id)

@router.get("/orders/{order_id}", response_model=OrderReadWithItems)
def get_order(
    order_id: int,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    return order_service.get_order_details(db, order_id, current_user)

@router.get("/shop/{shop_slug}/admin/orders", response_model=List[OrderReadWithItems])
def get_shop_orders(
    shop_slug: str,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user),
    shop = Depends(check_shop_active)
):
    return order_service.get_shop_orders(db, shop_slug, current_user)

@router.get("/platform/admin/orders", response_model=List[OrderReadWithItems])
def get_all_orders_admin(
    db: Session = Depends(get_db),
    admin = Depends(get_current_platform_admin)
):
    return order_service.get_all_orders_for_admin(db)

@router.put("/orders/{order_id}/status", response_model=OrderRead)
def update_order_status(
    order_id: int,
    status_update: OrderStatusUpdate,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    return order_service.update_order_status(db, order_id, status_update.status, current_user)

@router.put("/shop/{shop_slug}/admin/orders/{order_id}", response_model=OrderRead)
def update_order_status_shop(
    shop_slug: str,
    order_id: int,
    status_update: OrderStatusUpdate,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user),
    shop = Depends(check_shop_active)
):
    return order_service.update_order_status(db, order_id, status_update.status, current_user)
