from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app.db.session import get_db
from app.core.dependencies import get_current_user, get_current_platform_admin
from app.core.security import verify_password
from .service import ShopService
from .schemas import (
    ShopCreate, ShopRead, ShopReadWithOwner, ShopUpdate, DashboardStats, 
    ShopStatusUpdate, AdminActionRequest, TelegramBotTestRequest, 
    TelegramBotTestResponse, TelegramSyncChatRequest
)

router = APIRouter()
shop_service = ShopService()

@router.post("/platform/shops/register", response_model=ShopRead)
def register_shop(shop: ShopCreate, db: Session = Depends(get_db), current_user = Depends(get_current_user)):
    return shop_service.register_shop(db, shop, current_user.id)

@router.get("/platform/shops/me", response_model=List[ShopRead])
def get_my_shops(db: Session = Depends(get_db), current_user = Depends(get_current_user)):
    shop = shop_service.get_my_shops(db, current_user.id)
    if shop:
        shop = shop_service.prepare_for_read(shop)
        return [shop]
    return []

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
    # Public endpoint - but check if shop is active
    shop = shop_service.get_shop_by_slug(db, shop_slug, check_active=False)
    if not shop.is_active:
        raise HTTPException(status_code=403, detail="Shop is deactivated")
    return shop

@router.put("/shop/{shop_slug}/admin/info", response_model=ShopRead)
async def update_shop_settings(
    shop_slug: str, 
    shop_in: ShopUpdate, 
    db: Session = Depends(get_db), 
    current_user = Depends(get_current_user)
):
    shop = shop_service.update_shop(db, shop_slug, shop_in, current_user)
    
    # If telegram_bot_token exists and bot is active, set webhook
    # We use the token from the updated shop object (decrypted)
    if shop.telegram_bot_token and shop.is_bot_active:
        from app.core.crypto import crypto
        decrypted_token = crypto.decrypt(shop.telegram_bot_token)
        if decrypted_token:
            try:
                webhook_result = await shop_service.set_telegram_webhook(
                    decrypted_token, 
                    shop_slug
                )
                if webhook_result.get("success"):
                    print(f"✓ Webhook set for {shop_slug}: {webhook_result.get('webhook_url')}")
                else:
                    print(f"⚠ Failed to set webhook: {webhook_result.get('error')}")
            except Exception as e:
                print(f"⚠ Error setting webhook: {e}")
    
    return shop_service.prepare_for_read(shop)

@router.post("/shop/{shop_slug}/admin/telegram/test", response_model=TelegramBotTestResponse)
async def test_telegram_bot(
    shop_slug: str,
    request: TelegramBotTestRequest,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    # Check permissions
    shop = shop_service.get_shop_by_slug(db, shop_slug)
    if shop.owner_id != current_user.id and current_user.role != "platform_admin":
        raise HTTPException(status_code=403, detail="Not authorized")
    
    token_to_verify = request.token
    # If token appears to be the masked one from our DB
    if token_to_verify and "..." in token_to_verify and shop.telegram_bot_token:
        from app.core.crypto import crypto
        decrypted = crypto.decrypt(shop.telegram_bot_token)
        if decrypted:
            token_to_verify = decrypted
    
    return await shop_service.verify_bot_token(token_to_verify)

@router.post("/shop/{shop_slug}/telegram/sync")
def sync_chat_id(
    shop_slug: str,
    request: TelegramSyncChatRequest,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    shop_service.sync_telegram_chat(db, shop_slug, current_user.id, request.chat_id)
    return {"status": "success"}

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
