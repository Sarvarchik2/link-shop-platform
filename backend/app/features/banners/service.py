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
        return self.repository.get_by_shop_slug(db, shop_id=shop_id)

    def update_banner(self, db: Session, banner_in, shop_slug: str, current_user):
        shop_id = None
        if shop_slug:
            shop = self.shop_service.get_shop_by_slug(db, shop_slug)
            
            # Check permissions
            if current_user.role != "platform_admin" and shop.owner_id != current_user.id:
                from fastapi import HTTPException
                raise HTTPException(status_code=403, detail="Not authorized")
            
            shop_id = shop.id
        else:
            # Platform global banner
            if current_user.role != "platform_admin":
                from fastapi import HTTPException
                raise HTTPException(status_code=403, detail="Not authorized")
        
        # Check if banner exists for this shop
        from .models import Banner
        db_banner = db.query(Banner).filter(Banner.shop_id == shop_id).first()
        
        banner_data = banner_in.model_dump()
        banner_data["shop_id"] = shop_id
        
        if db_banner:
            return self.repository.update(db, db_banner, banner_data)
        else:
            return self.repository.create(db, banner_data)
