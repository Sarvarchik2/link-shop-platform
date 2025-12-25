from sqlalchemy.orm import Session
from sqlalchemy import or_
from .models import Product

class ProductRepository:
    def get_by_id(self, db: Session, product_id: int):
        return db.query(Product).filter(Product.id == product_id).first()

    def get_all(self, db: Session, skip: int = 0, limit: int = 100, shop_id: int = None, category: str = None, brand: str = None, query: str = None):
        q = db.query(Product)
        if shop_id:
            q = q.filter(Product.shop_id == shop_id)
        if category:
            q = q.filter(Product.category == category)
        if brand:
            q = q.filter(Product.brand == brand)
        if query:
            q = q.filter(or_(Product.name.contains(query), Product.description.contains(query)))
        return q.offset(skip).limit(limit).all()

    def create(self, db: Session, product_data: dict):
        db_product = Product(**product_data)
        db.add(db_product)
        db.commit()
        db.refresh(db_product)
        return db_product

    def update(self, db: Session, db_product: Product, update_data: dict):
        for field, value in update_data.items():
            setattr(db_product, field, value)
        db.commit()
        db.refresh(db_product)
        return db_product

    def delete(self, db: Session, db_product: Product):
        db.delete(db_product)
        db.commit()
        return True

    def count_by_shop(self, db: Session, shop_id: int):
        return db.query(Product).filter(Product.shop_id == shop_id).count()
