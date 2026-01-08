from sqlalchemy.orm import Session
from .repository import BannerRepository
from app.features.shops.service import ShopService

class BannerService:
    def __init__(self):
        self.repository = BannerRepository()
        self.shop_service = ShopService()

    def get_banners(self, db: Session, shop_slug: str = None):
        shop_id = None
        if shop_slug:
            shop = self.shop_service.get_shop_by_slug(db, shop_slug)
            shop_id = shop.id
        # Assuming repository returns list
        return self.repository.get_by_shop_slug(db, shop_id=shop_id)

    def get_banner(self, db: Session, banner_id: int, shop_slug: str, current_user):
        shop = self.shop_service.get_shop_by_slug(db, shop_slug, check_active=True)
        
        if current_user.role != "platform_admin" and shop.owner_id != current_user.id:
            from fastapi import HTTPException
            raise HTTPException(status_code=403, detail="Not authorized")
            
        banner = self.repository.get(db, banner_id)
        if not banner or banner.shop_id != shop.id:
            from fastapi import HTTPException
            raise HTTPException(status_code=404, detail="Banner not found")
            
        return banner

    def create_banner(self, db: Session, banner_in, shop_slug: str, current_user):
        shop = self.shop_service.get_shop_by_slug(db, shop_slug, check_active=True)
        
        # Permission check
        if current_user.role != "platform_admin" and shop.owner_id != current_user.id:
            from fastapi import HTTPException
            raise HTTPException(status_code=403, detail="Not authorized")

        # Check limit
        current_count = len(self.get_banners(db, shop_slug))
        
        # Get plan limit
        # Default to 1 if no plan or no limit set
        max_banners = 1
        if shop.subscription_plan_id:
            from app.features.subscriptions.models import SubscriptionPlan
            plan = db.query(SubscriptionPlan).get(shop.subscription_plan_id)
            if plan:
                max_banners = plan.max_banners or 1
        
        if current_count >= max_banners:
             from fastapi import HTTPException
             raise HTTPException(status_code=400, detail=f"Banner limit reached ({max_banners})")

        banner_data = banner_in.model_dump()
        banner_data["shop_id"] = shop.id
        return self.repository.create(db, banner_data)

    def update_banner(self, db: Session, banner_id: int, banner_in, shop_slug: str, current_user):
        shop = self.shop_service.get_shop_by_slug(db, shop_slug, check_active=True)
        
        if current_user.role != "platform_admin" and shop.owner_id != current_user.id:
            from fastapi import HTTPException
            raise HTTPException(status_code=403, detail="Not authorized")
            
        banner = self.repository.get(db, banner_id)
        if not banner or banner.shop_id != shop.id:
            from fastapi import HTTPException
            raise HTTPException(status_code=404, detail="Banner not found")
            
        banner_data = banner_in.model_dump(exclude_unset=True)
        return self.repository.update(db, banner, banner_data)

    def delete_banner(self, db: Session, banner_id: int, shop_slug: str, current_user):
        shop = self.shop_service.get_shop_by_slug(db, shop_slug, check_active=True)
        
        if current_user.role != "platform_admin" and shop.owner_id != current_user.id:
             from fastapi import HTTPException
             raise HTTPException(status_code=403, detail="Not authorized")

        banner = self.repository.get(db, banner_id)
        if not banner or banner.shop_id != shop.id:
             from fastapi import HTTPException
             raise HTTPException(status_code=404, detail="Banner not found")
             
        return self.repository.remove(db, id=banner_id)
