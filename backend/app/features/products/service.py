from sqlalchemy.orm import Session
from fastapi import HTTPException
from .repository import ProductRepository
from .schemas import ProductCreate, ProductUpdate
from app.features.shops.service import ShopService

class ProductService:
    def __init__(self):
        self.repository = ProductRepository()
        self.shop_service = ShopService()

    def get_products(self, db: Session, shop_slug: str = None, **kwargs):
        if shop_slug:
            shop = self.shop_service.get_shop_by_slug(db, shop_slug)
            kwargs["shop_id"] = shop.id
        # kwargs will contain sort_by, sort_order etc
        return self.repository.get_all(db, **kwargs)

    def get_product(self, db: Session, product_id: int):
        product = self.repository.get_by_id(db, product_id)
        if not product:
            raise HTTPException(status_code=404, detail="Product not found")
        return product

    def create_product(self, db: Session, product_in: ProductCreate, shop_slug: str, current_user):
        if not shop_slug:
            raise HTTPException(status_code=400, detail="shop_slug is required to create a product")
            
        shop = self.shop_service.get_shop_by_slug(db, shop_slug, check_active=True)
        
        # Check permissions
        if current_user.role != "platform_admin" and shop.owner_id != current_user.id:
            raise HTTPException(status_code=403, detail="Not authorized")
            
        # Check limits (optional logic from main.py)
        # For simplicity, just creating for now.
        
        product_data = product_in.model_dump()
        product_data["shop_id"] = shop.id
        return self.repository.create(db, product_data)

    def update_product(self, db: Session, product_id: int, product_in: ProductUpdate, current_user):
        product = self.get_product(db, product_id)
        shop = self.shop_service.get_shop_by_id(db, shop_id=product.shop_id, check_active=True) 
        
        if current_user.role != "platform_admin" and shop.owner_id != current_user.id:
            raise HTTPException(status_code=403, detail="Not authorized")
            
        update_data = product_in.model_dump(exclude_unset=True)
        return self.repository.update(db, product, update_data)

    def delete_product(self, db: Session, product_id: int, current_user):
        product = self.get_product(db, product_id)
        
        shop = self.shop_service.get_shop_by_id(db, shop_id=product.shop_id, check_active=True)
        if current_user.role != "platform_admin" and shop.owner_id != current_user.id:
            raise HTTPException(status_code=403, detail="Not authorized")
            
        return self.repository.delete(db, product)

    def toggle_favorite(self, db: Session, product_id: int):
        product = self.get_product(db, product_id)
        return self.repository.update(db, product, {"is_favorite": not product.is_favorite})
