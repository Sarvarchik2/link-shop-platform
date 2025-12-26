from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from typing import List, Optional
from datetime import datetime, timedelta
from .repository import SubscriptionRepository
from .schemas import (
    SubscriptionRequestCreate, SubscriptionPlanRead, SubscriptionRequestRead, 
    SubscriptionRequestUpdate, SubscriptionPlanCreate, SubscriptionPlanUpdate
)
from app.features.shops.service import ShopService
from app.features.shops.repository import ShopRepository

class SubscriptionService:
    def __init__(self):
        self.repository = SubscriptionRepository()
        self.shop_service = ShopService()
        self.shop_repository = ShopRepository()

    def get_plans(self, db: Session, active_only: bool = True):
        plans = self.repository.get_plans(db, active_only)
        result = []
        for plan in plans:
            plan_data = SubscriptionPlanRead.model_validate(plan)
            # The features_list processing is now handled by the field_validator in SubscriptionPlanRead schema
            # But we double check here if needed or just rely on validator. 
            # Given the validator logic, we don't need manual parsing here anymore if using standard Pydantic validation
            # ensuring from_attributes=True calls the validator.
            # However, validators with mode='before' and from_attributes might need care.
            # Let's manually ensure compatibility if the validator doesn't trigger on ORM objects directly
            if plan.features:
                 plan_data.features_list = [f.strip() for f in plan.features.split(",") if f.strip()]
            result.append(plan_data)
        return result

    def get_plan(self, db: Session, plan_id: int):
        plan = self.repository.get_plan_by_id(db, plan_id)
        if not plan:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Subscription plan not found"
            )
        return plan

    def create_plan(self, db: Session, plan_in: SubscriptionPlanCreate):
        return self.repository.create_plan(db, plan_in)

    def update_plan(self, db: Session, plan_id: int, plan_in: SubscriptionPlanUpdate):
        plan = self.get_plan(db, plan_id)
        return self.repository.update_plan(db, plan, plan_in)

    def delete_plan(self, db: Session, plan_id: int):
        plan = self.get_plan(db, plan_id)
        return self.repository.delete_plan(db, plan)

    def create_subscription_request(self, db: Session, shop_slug: str, request_in: SubscriptionRequestCreate, current_user):
        shop = self.shop_service.get_shop_by_slug(db, shop_slug)
        if shop.owner_id != current_user.id and current_user.role != "platform_admin":
            raise HTTPException(status_code=403, detail="Not authorized")
            
        # Check if plan exists
        plan = self.repository.get_plan_by_id(db, request_in.plan_id)
        if not plan:
            raise HTTPException(status_code=404, detail="Plan not found")
        
        # Check for existing pending request
        from .models import SubscriptionRequest
        existing_request = db.query(SubscriptionRequest).filter(
            SubscriptionRequest.shop_id == shop.id,
            SubscriptionRequest.status == "pending"
        ).first()
        
        if existing_request:
            raise HTTPException(
                status_code=400, 
                detail="У вас уже есть активный запрос на подписку. Дождитесь ответа администратора."
            )
            
        request_data = request_in.model_dump()
        request_data["shop_id"] = shop.id
        request_data["status"] = "pending"
        
        db_request = self.repository.create_request(db, request_data)
        return self._populate_request_details(db, db_request)

    def get_shop_subscription_request(self, db: Session, shop_slug: str, current_user):
        shop = self.shop_service.get_shop_by_slug(db, shop_slug)
        if shop.owner_id != current_user.id and current_user.role != "platform_admin":
            raise HTTPException(status_code=403, detail="Not authorized")
            
        db_request = self.repository.get_request_by_shop(db, shop.id)
        if not db_request:
            return None
            
        return self._populate_request_details(db, db_request)

    def get_all_requests(self, db: Session, status: Optional[str] = None, shop_id: Optional[int] = None):
        """Get all subscription requests - for platform admin"""
        requests = self.repository.get_all_requests(db, status, shop_id)
        result = []
        for req in requests:
            result.append(self._populate_request_details(db, req))
        return result

    def update_request_status(self, db: Session, request_id: int, update_in: SubscriptionRequestUpdate):
        """Approve or reject subscription request - for platform admin"""
        db_request = self.repository.get_request_by_id(db, request_id)
        if not db_request:
            raise HTTPException(status_code=404, detail="Subscription request not found")
        
        if update_in.status not in ["approved", "rejected"]:
            raise HTTPException(status_code=400, detail="Status must be 'approved' or 'rejected'")
        
        update_data = {
            "status": update_in.status,
            "approved_at": datetime.utcnow() if update_in.status == "approved" else None
        }
        
        if update_in.notes:
            update_data["notes"] = update_in.notes
        
        # If approved, update shop subscription
        if update_in.status == "approved":
            shop = self.shop_repository.get_by_id(db, db_request.shop_id)
            plan = self.repository.get_plan_by_id(db, db_request.plan_id)
            
            if shop and plan:
                # Calculate expiration date
                now = datetime.utcnow()
                if shop.subscription_status == "active" and shop.subscription_expires_at and shop.subscription_expires_at > now:
                     # Extend existing subscription
                     expires_at = shop.subscription_expires_at + timedelta(days=30 * db_request.duration_months)
                else:
                     # New or renewed from expired
                     expires_at = now + timedelta(days=30 * db_request.duration_months)
                
                shop_update_data = {
                    "subscription_status": "active",
                    "subscription_expires_at": expires_at,
                    "subscription_plan_id": plan.id
                }
                
                self.shop_repository.update(db, shop, shop_update_data)
        
        updated_request = self.repository.update_request(db, db_request, update_data)
        return self._populate_request_details(db, updated_request)

    def _populate_request_details(self, db: Session, request):
        """Helper to populate plan and shop details"""
        if not request:
            return None
        
        plan = self.repository.get_plan_by_id(db, request.plan_id)
        shop = self.shop_repository.get_by_id(db, request.shop_id)
        
        request_read = SubscriptionRequestRead.model_validate(request)
        if plan:
            request_read.plan_name = plan.name
        if shop:
            request_read.shop_name = shop.name
            request_read.shop_slug = shop.slug
            
        return request_read

    def cancel_subscription(self, db: Session, shop_slug: str, current_user):
        """Cancel subscription - shop owner only"""
        shop = self.shop_service.get_shop_by_slug(db, shop_slug)
        if shop.owner_id != current_user.id and current_user.role != "platform_admin":
            raise HTTPException(status_code=403, detail="Not authorized")
        
        if shop.subscription_status != "active":
            raise HTTPException(status_code=400, detail="Подписка не активна")
        
        # Update shop subscription status to cancelled
        shop_update_data = {
            "subscription_status": "cancelled"
        }
        
        self.shop_repository.update(db, shop, shop_update_data)
        
        return {"message": "Подписка успешно отменена"}
