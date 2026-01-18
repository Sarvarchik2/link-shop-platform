from fastapi import APIRouter, Depends, HTTPException, status, BackgroundTasks
from sqlalchemy.orm import Session
from typing import List
from datetime import datetime
from app.db.session import get_db
from app.core.dependencies import get_current_user
from app.features.users.models import User
from app.features.shops.repository import ShopRepository
from . import schemas, service, models, tasks
import logging

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/shop/{shop_slug}/admin/broadcasts")
shop_repo = ShopRepository()

async def get_shop_and_check_permission(shop_slug: str, db: Session, current_user: User):
    shop = shop_repo.get_by_slug(db, shop_slug)
    if not shop:
        raise HTTPException(status_code=404, detail="Shop not found")
    if shop.owner_id != current_user.id and current_user.role != "platform_admin":
        raise HTTPException(status_code=403, detail="Not enough permissions")
             
    return shop

def check_broadcast_permission(shop, db, current_user):
    from app.features.subscriptions.models import SubscriptionPlan
    plan = db.query(SubscriptionPlan).filter(SubscriptionPlan.id == shop.subscription_plan_id).first()
    if not plan or not plan.can_broadcast:
        if current_user.role != "platform_admin":
             raise HTTPException(status_code=403, detail="Your current plan does not support broadcasts")

@router.get("", response_model=List[schemas.BroadcastResponse])
async def list_broadcasts(
    shop_slug: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    shop = await get_shop_and_check_permission(shop_slug, db, current_user)
    return service.broadcast_service.get_shop_broadcasts(db, shop.id)

@router.post("", response_model=schemas.BroadcastResponse)
async def create_broadcast(
    shop_slug: str,
    broadcast_in: schemas.BroadcastCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    shop = await get_shop_and_check_permission(shop_slug, db, current_user)
    check_broadcast_permission(shop, db, current_user)
    try:
        return service.broadcast_service.create_broadcast(db, shop.id, broadcast_in.dict())
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/{broadcast_id}/send", response_model=schemas.BroadcastResponse)
async def send_broadcast(
    shop_slug: str,
    broadcast_id: int,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    shop = await get_shop_and_check_permission(shop_slug, db, current_user)
    check_broadcast_permission(shop, db, current_user)
    broadcast = service.broadcast_service.get_broadcast(db, broadcast_id)
    
    if not broadcast:
        raise HTTPException(status_code=404, detail="Broadcast not found")
    if broadcast.shop_id != shop.id:
        raise HTTPException(status_code=400, detail="Invalid broadcast for this shop")
    if broadcast.status != models.BroadcastStatus.DRAFT:
        raise HTTPException(status_code=400, detail="Broadcast can only be sent from DRAFT status")

    # Update status to PENDING
    broadcast = service.broadcast_service.update_broadcast(db, broadcast, {"status": models.BroadcastStatus.PENDING})
    
    # Try Celery first, fallback to BackgroundTasks if Redis is missing or unresponsive
    try:
        from app.core.celery_app import celery_app
        import redis
        from app.core.config import settings
        
        broker_url = celery_app.conf.broker_url
        is_redis = broker_url and (broker_url.startswith("redis://") or broker_url.startswith("rediss://"))
        
        if is_redis:
            # Check if redis is actually reachable to avoid long waits/retries
            try:
                # Use a short timeout for the check
                r = redis.from_url(broker_url, socket_timeout=2, socket_connect_timeout=2)
                r.ping()
                
                from app.features.broadcasts import tasks
                tasks.send_broadcast_task.delay(broadcast.id)
                logger.info(f"Broadcast {broadcast.id} queued via Celery")
                return broadcast
            except Exception as redis_err:
                logger.debug("Redis unavailable, using BackgroundTasks")
                # Fall through to BackgroundTasks
        
        from app.features.broadcasts import tasks
        background_tasks.add_task(tasks.send_broadcast_task, broadcast.id)
        logger.info(f"Broadcast {broadcast.id} queued via BackgroundTasks")
        
    except Exception as e:
        logger.error(f"Celery setup/delivery failed, using BackgroundTasks: {e}")
        from app.features.broadcasts import tasks
        background_tasks.add_task(tasks.send_broadcast_task, broadcast.id)
    
    return broadcast

@router.get("/debug/subscribers")
async def get_subscribers_count(
    shop_slug: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Debug endpoint to check subscriber count"""
    from app.features.shops.models import UserStoreTelegram
    
    shop = await get_shop_and_check_permission(shop_slug, db, current_user)
    
    # Get all subscribers
    all_subscribers = db.query(UserStoreTelegram).filter(
        UserStoreTelegram.store_id == shop.id
    ).all()
    
    # Get recent subscribers (with orders in last 30 days)
    from app.features.orders.models import Order
    from datetime import timedelta
    thirty_days_ago = datetime.utcnow()
    
    recent_subscribers = db.query(UserStoreTelegram).join(
        Order, Order.user_id == UserStoreTelegram.user_id
    ).filter(
        UserStoreTelegram.store_id == shop.id,
        Order.shop_id == shop.id,
        Order.created_at >= thirty_days_ago
    ).distinct().all()
    
    return {
        "shop_id": shop.id,
        "shop_slug": shop.slug,
        "total_subscribers": len(all_subscribers),
        "recent_subscribers": len(recent_subscribers),
        "subscribers": [
            {
                "user_id": s.user_id,
                "chat_id": s.telegram_chat_id
            } for s in all_subscribers
        ]
    }

@router.delete("/{broadcast_id}")
async def delete_broadcast(
    shop_slug: str,
    broadcast_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    shop = await get_shop_and_check_permission(shop_slug, db, current_user)
    broadcast = service.broadcast_service.get_broadcast(db, broadcast_id)
    
    if not broadcast:
        raise HTTPException(status_code=404, detail="Broadcast not found")
    if broadcast.shop_id != shop.id:
        raise HTTPException(status_code=400, detail="Invalid broadcast for this shop")
    
    db.delete(broadcast)
    db.commit()
    return {"status": "ok"}
