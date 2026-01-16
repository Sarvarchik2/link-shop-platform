from fastapi import APIRouter, Depends, HTTPException, status, BackgroundTasks
from sqlalchemy.orm import Session
from typing import List
from app.db.session import get_db
from app.core.dependencies import get_current_user
from app.features.users.models import User
from app.features.shops.repository import ShopRepository
from . import schemas, service, models, tasks

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
    
    # Try Celery first, fallback to BackgroundTasks if Redis is missing
    try:
        from app.core.celery_app import celery_app
        import redis
        from app.core.config import settings
        
        # Simple check if redis is reachable
        r = redis.from_url(settings.DATABASE_URL.replace("sqlite", "redis") if "redis" not in os.getenv("REDIS_URL", "") else os.getenv("REDIS_URL")) # Simplified
        # Better check:
        broker_url = celery_app.conf.broker_url
        if broker_url.startswith("redis"):
             tasks.send_broadcast_task.delay(broadcast.id)
        else:
             background_tasks.add_task(tasks.send_broadcast_task, broadcast.id)
    except Exception as e:
        print(f"Celery delivery failed, using BackgroundTasks: {e}")
        background_tasks.add_task(tasks.send_broadcast_task, broadcast.id)
    
    return broadcast

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
