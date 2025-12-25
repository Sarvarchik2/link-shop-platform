from sqlalchemy.orm import Session
from typing import Optional
from .models import Banner

class BannerRepository:
    def get_by_shop_slug(self, db: Session, shop_id: Optional[int]):
        # Try to find shop-specific banners first
        banners = db.query(Banner).filter(Banner.shop_id == shop_id, Banner.is_active == True).all()
        
        # If no shop-specific banners found and we were looking for a specific shop, try global banners
        if not banners and shop_id is not None:
            banners = db.query(Banner).filter(Banner.shop_id == None, Banner.is_active == True).all()
            
        return banners

    def create(self, db: Session, banner_data: dict):
        db_banner = Banner(**banner_data)
        db.add(db_banner)
        db.commit()
        db.refresh(db_banner)
        return db_banner

    def update(self, db: Session, db_banner: Banner, update_data: dict):
        for field, value in update_data.items():
            setattr(db_banner, field, value)
        db.commit()
        db.refresh(db_banner)
        return db_banner
