from sqlalchemy.orm import Session
from typing import List, Optional
from .models import SubscriptionPlan, SubscriptionRequest

class SubscriptionRepository:
    def get_plans(self, db: Session, active_only: bool = True) -> List[SubscriptionPlan]:
        q = db.query(SubscriptionPlan)
        if active_only:
            q = q.filter(SubscriptionPlan.is_active == True)
        return q.order_by(SubscriptionPlan.display_order).all()

    def get_plan_by_id(self, db: Session, plan_id: int) -> Optional[SubscriptionPlan]:
        return db.query(SubscriptionPlan).filter(SubscriptionPlan.id == plan_id).first()

    def create_request(self, db: Session, request_data: dict) -> SubscriptionRequest:
        db_request = SubscriptionRequest(**request_data)
        db.add(db_request)
        db.commit()
        db.refresh(db_request)
        return db_request

    def get_request_by_shop(self, db: Session, shop_id: int) -> Optional[SubscriptionRequest]:
        return db.query(SubscriptionRequest).\
            filter(SubscriptionRequest.shop_id == shop_id).\
            order_by(SubscriptionRequest.requested_at.desc()).\
            first()

    def get_all_requests(self, db: Session, status: Optional[str] = None) -> List[SubscriptionRequest]:
        q = db.query(SubscriptionRequest)
        if status:
            q = q.filter(SubscriptionRequest.status == status)
        return q.order_by(SubscriptionRequest.requested_at.desc()).all()

    def get_request_by_id(self, db: Session, request_id: int) -> Optional[SubscriptionRequest]:
        return db.query(SubscriptionRequest).filter(SubscriptionRequest.id == request_id).first()

    def update_request(self, db: Session, db_request: SubscriptionRequest, update_data: dict) -> SubscriptionRequest:
        for field, value in update_data.items():
            setattr(db_request, field, value)
        db.commit()
        db.refresh(db_request)
        return db_request
