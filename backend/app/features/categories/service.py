from sqlalchemy.orm import Session
from fastapi import HTTPException
from .repository import CategoryRepository
from app.features.shops.service import ShopService

class CategoryService:
    def __init__(self):
        self.repository = CategoryRepository()
        self.shop_service = ShopService()

    def get_categories(self, db: Session, shop_slug: str = None):
        shop_id = None
        if shop_slug:
            shop = self.shop_service.get_shop_by_slug(db, shop_slug)
            shop_id = shop.id
        return self.repository.get_all(db, shop_id=shop_id)

    def create_category(self, db: Session, category_in, shop_slug: str, current_user):
        shop_id = None
        if shop_slug:
            shop = self.shop_service.get_shop_by_slug(db, shop_slug, check_active=True)
            if current_user.role != "platform_admin" and shop.owner_id != current_user.id:
                raise HTTPException(status_code=403, detail="Not authorized")
            shop_id = shop.id
        else:
            if current_user.role != "platform_admin":
                raise HTTPException(status_code=403, detail="Not authorized")
        
        category_data = category_in.model_dump()
        category_data["shop_id"] = shop_id
        return self.repository.create(db, category_data)

    def update_category(self, db: Session, category_id: int, category_in, current_user):
        category = self.repository.get_by_id(db, category_id)
        if not category:
            raise HTTPException(status_code=404, detail="Category not found")
        
        if category.shop_id:
            shop = self.shop_service.get_shop_by_id(db, category.shop_id, check_active=True)
            if current_user.role != "platform_admin" and shop.owner_id != current_user.id:
                raise HTTPException(status_code=403, detail="Not authorized")
        else:
            if current_user.role != "platform_admin":
                raise HTTPException(status_code=403, detail="Not authorized")
                
        update_data = category_in.model_dump(exclude_unset=True)
        return self.repository.update(db, category, update_data)

    def delete_category(self, db: Session, category_id: int, current_user):
        category = self.repository.get_by_id(db, category_id)
        if not category:
            raise HTTPException(status_code=404, detail="Category not found")

        if category.shop_id:
            shop = self.shop_service.get_shop_by_id(db, category.shop_id, check_active=True)
            if current_user.role != "platform_admin" and shop.owner_id != current_user.id:
                raise HTTPException(status_code=403, detail="Not authorized")
        else:
            if current_user.role != "platform_admin":
                raise HTTPException(status_code=403, detail="Not authorized")
                
        return self.repository.delete(db, category)
