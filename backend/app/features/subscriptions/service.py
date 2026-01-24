from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from typing import List, Optional
from datetime import datetime, timedelta
from .repository import SubscriptionRepository
from .schemas import (
    SubscriptionRequestCreate, SubscriptionPlanRead, SubscriptionRequestRead, 
    SubscriptionRequestUpdate, SubscriptionPlanCreate, SubscriptionPlanUpdate,
    SubscriptionPurchaseRequest, SubscriptionPurchaseResponse,
    AutoRenewalToggleRequest, AutoRenewalToggleResponse
)
from app.features.shops.service import ShopService
from app.features.shops.repository import ShopRepository
from decimal import Decimal

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
        
        if update_in.status == "approved":
            shop = self.shop_repository.get_by_id(db, db_request.shop_id)
            plan = self.repository.get_plan_by_id(db, db_request.plan_id)
            
            if shop and plan:
                now = datetime.utcnow()
                
                # Logic based on request type
                period = plan.trial_period_days if plan.is_trial and plan.trial_period_days > 0 else plan.period_days
                if period <= 0: period = 30
                
                if db_request.type == "renew":
                    # Extend existing subscription
                    if shop.subscription_expires_at and shop.subscription_expires_at > now:
                        # If active, add to current expiry
                        expires_at = shop.subscription_expires_at + timedelta(days=period * db_request.duration_months)
                    else:
                        # If expired, start from now
                        expires_at = now + timedelta(days=period * db_request.duration_months)
                    subscription_plan_id = db_request.plan_id
                    
                elif db_request.type == "change":
                    expires_at = now + timedelta(days=period * db_request.duration_months)
                    subscription_plan_id = db_request.plan_id
                    
                else: # Default/New
                    expires_at = now + timedelta(days=period * db_request.duration_months)
                    subscription_plan_id = db_request.plan_id
                
                shop_update_data = {
                    "subscription_status": "trial" if plan.is_trial else "active",
                    "subscription_expires_at": expires_at,
                    "subscription_plan_id": subscription_plan_id
                }

                if plan.is_trial:
                    used_trials = list(shop.used_trials_json or [])
                    if plan.id not in used_trials:
                        used_trials.append(plan.id)
                    shop_update_data["used_trials_json"] = used_trials
                
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

    def purchase_subscription(
        self, 
        db: Session, 
        shop_slug: str, 
        request: SubscriptionPurchaseRequest, 
        current_user
    ) -> SubscriptionPurchaseResponse:
        """Purchase subscription using wallet balance"""
        from app.features.wallet.service import WalletService
        
        # Get shop and verify ownership
        shop = self.shop_service.get_shop_by_slug(db, shop_slug)
        if shop.owner_id != current_user.id and current_user.role != "platform_admin":
            raise HTTPException(status_code=403, detail="Not authorized")
        
        # Get plan
        plan = self.repository.get_plan_by_slug(db, request.plan_slug)
        if not plan:
            raise HTTPException(status_code=404, detail="План не найден")
        
        # Calculate price with period discount
        period_multipliers = {
            1: 1.0,      # No discount
            3: 0.90,     # 10% discount
            6: 0.80,     # 20% discount
            12: 0.70     # 30% discount
        }
        
        if request.period_months not in period_multipliers:
            raise HTTPException(
                status_code=400, 
                detail="Период должен быть 1, 3, 6 или 12 месяцев"
            )
        
        multiplier = period_multipliers[request.period_months]
        total_price = Decimal(str(plan.price * request.period_months * multiplier))
        
        # Check and charge wallet
        wallet_service = WalletService(db)
        
        if not wallet_service.has_sufficient_balance(shop.id, total_price):
            raise HTTPException(
                status_code=402,
                detail=f"Недостаточно средств. Требуется: {total_price} сум"
            )
        
        success, transaction = wallet_service.charge(
            shop_id=shop.id,
            amount=total_price,
            description=f"Оплата подписки {plan.name} на {request.period_months} мес.",
            meta_data={
                "plan_slug": request.plan_slug,
                "period_months": request.period_months,
                "payment_method": request.payment_method
            }
        )

        
        if not success:
            raise HTTPException(
                status_code=500,
                detail="Ошибка при списании средств"
            )
        
        # Update shop subscription
        now = datetime.utcnow()
        
        # If active subscription exists for THE SAME PLAN and not expired, extend from current expiry
        is_same_plan = shop.subscription_plan_id == plan.id
        if is_same_plan and shop.subscription_status == "active" and shop.subscription_expires_at and shop.subscription_expires_at > now:
            expires_at = shop.subscription_expires_at + timedelta(days=30 * request.period_months)
        else:
            # If plan changed or expired, start new subscription from now (burn current time)
            expires_at = now + timedelta(days=30 * request.period_months)
        
        shop_update_data = {
            "subscription_status": "active",
            "subscription_expires_at": expires_at,
            "subscription_plan_id": plan.id,
            "subscription_period_months": request.period_months
        }
        
        self.shop_repository.update(db, shop, shop_update_data)
        
        return SubscriptionPurchaseResponse(
            success=True,
            subscription_id=plan.id,
            expires_at=expires_at,
            message=f"Подписка успешно активирована до {expires_at.strftime('%d.%m.%Y')}"
        )

    def toggle_auto_renewal(
        self,
        db: Session,
        shop_slug: str,
        request: AutoRenewalToggleRequest,
        current_user
    ) -> AutoRenewalToggleResponse:
        """Toggle auto-renewal for subscription"""
        shop = self.shop_service.get_shop_by_slug(db, shop_slug)
        if shop.owner_id != current_user.id and current_user.role != "platform_admin":
            raise HTTPException(status_code=403, detail="Not authorized")
        
        shop_update_data = {
            "auto_renewal_enabled": request.enabled
        }
        
        self.shop_repository.update(db, shop, shop_update_data)
        
        message = "Автопродление включено" if request.enabled else "Автопродление выключено"
        
        return AutoRenewalToggleResponse(
            auto_renewal_enabled=request.enabled,
            message=message
        )

    def start_trial(self, db: Session, shop_slug: str, plan_slug: str, current_user):
        """Start a trial period for a specific plan"""
        shop = self.shop_service.get_shop_by_slug(db, shop_slug)
        if shop.owner_id != current_user.id and current_user.role != "platform_admin":
            raise HTTPException(status_code=403, detail="Not authorized")
        
        plan = self.repository.get_plan_by_slug(db, plan_slug)
        if not plan:
            raise HTTPException(status_code=404, detail="План не найден")
        
        if not plan.is_active:
            raise HTTPException(status_code=400, detail="План не активен")
        
        if not plan.is_trial and plan.price > 0:
            # If plan doesn't have is_trial=True, but has price, 
            # we check if TRIAL as a concept is allowed for this paid plan.
            # In our current logic, we allow trial if trial_period_days > 0.
            if plan.trial_period_days <= 0:
                raise HTTPException(status_code=400, detail="Для этого тарифа не предусмотрен пробный период")
        
        # Check if trial already used for this specific plan
        used_trials = shop.used_trials_json or []
        if plan.id in used_trials:
            raise HTTPException(
                status_code=400, 
                detail="Вы уже использовали пробный период для этого тарифа"
            )
        
        # Update shop
        now = datetime.utcnow()
        trial_days = plan.trial_period_days if plan.trial_period_days > 0 else 7
        expires_at = now + timedelta(days=trial_days)
        
        # Add to used trials
        new_used_trials = list(used_trials)
        new_used_trials.append(plan.id)
        
        shop_update_data = {
            "subscription_status": "trial",
            "subscription_expires_at": expires_at,
            "subscription_plan_id": plan.id,
            "used_trials_json": new_used_trials
        }
        
        self.shop_repository.update(db, shop, shop_update_data)
        
        return {
            "success": True,
            "message": f"Пробный период для тарифа {plan.name} активирован на {trial_days} дней",
            "expires_at": expires_at
        }

