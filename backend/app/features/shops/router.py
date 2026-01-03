from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app.db.session import get_db
from app.core.dependencies import get_current_user, get_current_platform_admin
from app.core.security import verify_password
from .service import ShopService
from .schemas import ShopCreate, ShopRead, ShopReadWithOwner, ShopUpdate, DashboardStats, ShopStatusUpdate, AdminActionRequest

router = APIRouter()
shop_service = ShopService()

@router.post("/platform/shops/register", response_model=ShopRead)
def register_shop(shop: ShopCreate, db: Session = Depends(get_db), current_user = Depends(get_current_user)):
    return shop_service.register_shop(db, shop, current_user.id)

@router.get("/platform/shops/me", response_model=List[ShopRead])
def get_my_shops(db: Session = Depends(get_db), current_user = Depends(get_current_user)):
    shop = shop_service.get_my_shops(db, current_user.id)
    return [shop] if shop else []

@router.get("/platform/shops", response_model=List[ShopReadWithOwner])
def get_all_shops(db: Session = Depends(get_db), admin = Depends(get_current_platform_admin)):
    return shop_service.get_all_shops_for_admin(db)

@router.get("/platform/admin/shops/{shop_id}", response_model=ShopReadWithOwner)
def get_shop_admin_details(
    shop_id: int, 
    db: Session = Depends(get_db), 
    admin = Depends(get_current_platform_admin)
):
    return shop_service.get_shop_details_for_admin(db, shop_id)

@router.get("/platform/shops/{shop_slug}", response_model=ShopRead)
def get_shop(shop_slug: str, db: Session = Depends(get_db)):
    return shop_service.get_shop_by_slug(db, shop_slug, check_active=True)

@router.put("/shop/{shop_slug}/admin/info", response_model=ShopRead)
def update_shop_settings(
    shop_slug: str, 
    shop_in: ShopUpdate, 
    db: Session = Depends(get_db), 
    current_user = Depends(get_current_user)
):
    return shop_service.update_shop(db, shop_slug, shop_in, current_user)

@router.get("/shop/{shop_slug}/admin/stats", response_model=DashboardStats)
def get_shop_admin_stats(
    shop_slug: str, 
    db: Session = Depends(get_db), 
    current_user = Depends(get_current_user)
):
    return shop_service.get_shop_stats(db, shop_slug, current_user)

@router.get("/platform/admin/stats", response_model=DashboardStats)
def get_platform_admin_stats(
    db: Session = Depends(get_db), 
    current_user = Depends(get_current_platform_admin)
):
    return shop_service.get_platform_stats(db)

@router.put("/platform/admin/shops/{shop_id}/subscription", response_model=ShopRead)
def update_shop_subscription(
    shop_id: int,
    shop_in: ShopUpdate,
    db: Session = Depends(get_db),
    admin = Depends(get_current_platform_admin)
):
    """Update shop subscription - platform admin only"""
    shop = shop_service.get_shop_by_id(db, shop_id)
    update_data = shop_in.model_dump(exclude_unset=True)
    return shop_service.repository.update(db, shop, update_data)

@router.put("/platform/admin/shops/{shop_id}/activate", response_model=ShopRead)
def toggle_shop_active(
    shop_id: int,
    status_update: ShopStatusUpdate,
    db: Session = Depends(get_db),
    admin = Depends(get_current_platform_admin)
):
    """Activate/deactivate shop - platform admin only"""
    if not verify_password(status_update.password, admin.password_hash):
        raise HTTPException(status_code=403, detail="Invalid password")

    shop = shop_service.get_shop_by_id(db, shop_id)
    return shop_service.repository.update(db, shop, {"is_active": status_update.is_active})

@router.post("/platform/admin/shops/{shop_id}/delete")
def delete_shop(
    shop_id: int,
    action: AdminActionRequest,
    db: Session = Depends(get_db),
    admin = Depends(get_current_platform_admin)
):
    """Delete shop - platform admin only"""
    if not verify_password(action.password, admin.password_hash):
        raise HTTPException(status_code=403, detail="Invalid password")
    
    shop_service.delete_shop(db, shop_id)
    return {"status": "success", "message": "Shop deleted"}
