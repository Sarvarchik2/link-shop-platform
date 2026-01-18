from sqlalchemy.orm import Session
from datetime import datetime, timedelta
from .models import Broadcast, BroadcastStatus, BroadcastAudience
from app.features.shops.models import Shop, UserStoreTelegram
from app.core.crypto import crypto
import logging

logger = logging.getLogger(__name__)

class BroadcastService:
    def create_broadcast(self, db: Session, shop_id: int, data: dict):
        # Check limit: 1 broadcast per 24 hours
        last_broadcast = db.query(Broadcast).filter(
            Broadcast.shop_id == shop_id,
            Broadcast.created_at >= datetime.utcnow() - timedelta(hours=24)
        ).first()
        
        # if last_broadcast:
        #     raise Exception("Only one broadcast allowed per 24 hours")

        # Calculate total_count based on audience_type
        audience_type = data.get('audience_type', BroadcastAudience.ALL)
        
        if audience_type == BroadcastAudience.RECENT or audience_type == 'recent':
            # Count users with orders in last 30 days
            from app.features.orders.models import Order
            thirty_days_ago = datetime.utcnow() - timedelta(days=30)
            
            total_count = db.query(UserStoreTelegram).join(
                Order, Order.user_id == UserStoreTelegram.user_id
            ).filter(
                UserStoreTelegram.store_id == shop_id,
                Order.shop_id == shop_id,
                Order.created_at >= thirty_days_ago
            ).distinct().count()
        else:
            # Count all subscribers
            total_count = db.query(UserStoreTelegram).filter(
                UserStoreTelegram.store_id == shop_id
            ).count()
        
        # Add total_count to data
        data['total_count'] = total_count
        logger.info(f"Creating broadcast for shop {shop_id} with {total_count} recipients (audience: {audience_type})")

        db_broadcast = Broadcast(shop_id=shop_id, **data)
        db.add(db_broadcast)
        db.commit()
        db.refresh(db_broadcast)
        return db_broadcast

    def get_shop_broadcasts(self, db: Session, shop_id: int):
        return db.query(Broadcast).filter(Broadcast.shop_id == shop_id).order_by(Broadcast.created_at.desc()).all()

    def get_broadcast(self, db: Session, broadcast_id: int):
        return db.query(Broadcast).filter(Broadcast.id == broadcast_id).first()

    def update_broadcast(self, db: Session, db_broadcast: Broadcast, data: dict):
        for field, value in data.items():
            setattr(db_broadcast, field, value)
        db.commit()
        db.refresh(db_broadcast)
        return db_broadcast

broadcast_service = BroadcastService()
