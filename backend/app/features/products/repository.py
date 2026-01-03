from sqlalchemy.orm import Session
from sqlalchemy import or_
from .models import Product

class ProductRepository:
    def get_by_id(self, db: Session, product_id: int):
        return db.query(Product).filter(Product.id == product_id).first()

    def get_all(self, db: Session, skip: int = 0, limit: int = 100, shop_id: int = None, category: str = None, brand: str = None, query: str = None, sort_by: str = None, sort_order: str = "desc"):
        q = db.query(Product)
        if shop_id:
            q = q.filter(Product.shop_id == shop_id)
        if category:
            q = q.filter(Product.category == category)
        if brand:
            q = q.filter(Product.brand == brand)
        if query:
            q = q.filter(or_(
                Product.name_en.ilike(f"%{query}%"),
                Product.name_ru.ilike(f"%{query}%"),
                Product.name_uz.ilike(f"%{query}%"),
                Product.description_en.ilike(f"%{query}%"),
                Product.description_ru.ilike(f"%{query}%"),
                Product.description_uz.ilike(f"%{query}%")
            ))
            
        # Sorting
        if sort_by:
            field = None
            if sort_by == 'price':
                field = Product.price
            elif sort_by == 'name':
                field = Product.name_en # Default to English for sorting
            elif sort_by == 'sold_count':
                field = Product.sold_count
            elif sort_by == 'stock':
                field = Product.stock
            elif sort_by == 'created_at':
                field = Product.created_at
            
            if field is not None:
                if sort_order == 'asc':
                    q = q.order_by(field.asc())
                else:
                    q = q.order_by(field.desc())
        else:
            # Default sort
            q = q.order_by(Product.created_at.desc())

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
