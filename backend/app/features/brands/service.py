from sqlalchemy.orm import Session
from fastapi import HTTPException
from .repository import BrandRepository
from app.features.shops.service import ShopService

class BrandService:
    def __init__(self):
        self.repository = BrandRepository()
        self.shop_service = ShopService()

    def get_brands(self, db: Session, shop_slug: str = None):
        shop_id = None
        if shop_slug:
            shop = self.shop_service.get_shop_by_slug(db, shop_slug)
            shop_id = shop.id
        return self.repository.get_all(db, shop_id=shop_id)

    def create_brand(self, db: Session, brand_in, shop_slug: str, current_user):
        shop_id = None
        if shop_slug:
            shop = self.shop_service.get_shop_by_slug(db, shop_slug, check_active=True)
            if current_user.role != "platform_admin" and shop.owner_id != current_user.id:
                raise HTTPException(status_code=403, detail="Not authorized")
            shop_id = shop.id
        else:
            if current_user.role != "platform_admin":
                raise HTTPException(status_code=403, detail="Not authorized")
        
        brand_data = brand_in.model_dump()
        brand_data["shop_id"] = shop_id
        return self.repository.create(db, brand_data)

    def update_brand(self, db: Session, brand_id: int, brand_in, current_user):
        brand = self.repository.get_by_id(db, brand_id)
        if not brand:
            raise HTTPException(status_code=404, detail="Brand not found")
        
        if brand.shop_id:
            shop = self.shop_service.get_shop_by_id(db, brand.shop_id, check_active=True)
            if current_user.role != "platform_admin" and shop.owner_id != current_user.id:
                raise HTTPException(status_code=403, detail="Not authorized")
        else:
            if current_user.role != "platform_admin":
                raise HTTPException(status_code=403, detail="Not authorized")
                
        update_data = brand_in.model_dump(exclude_unset=True)
        return self.repository.update(db, brand, update_data)

    def delete_brand(self, db: Session, brand_id: int, current_user):
        brand = self.repository.get_by_id(db, brand_id)
        if not brand:
            raise HTTPException(status_code=404, detail="Brand not found")

        if brand.shop_id:
            shop = self.shop_service.get_shop_by_id(db, brand.shop_id, check_active=True)
            if current_user.role != "platform_admin" and shop.owner_id != current_user.id:
                raise HTTPException(status_code=403, detail="Not authorized")
        else:
            if current_user.role != "platform_admin":
                raise HTTPException(status_code=403, detail="Not authorized")
                
        return self.repository.delete(db, brand)
