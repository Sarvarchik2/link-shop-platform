from sqlalchemy.orm import Session
from .models import Brand

class BrandRepository:
    def get_all(self, db: Session, shop_id: int = None):
        q = db.query(Brand)
        if shop_id:
            q = q.filter(Brand.shop_id == shop_id)
        else:
            q = q.filter(Brand.shop_id == None)
        return q.all()

    def create(self, db: Session, brand_data: dict):
        db_brand = Brand(**brand_data)
        db.add(db_brand)
        db.commit()
        db.refresh(db_brand)
        return db_brand

    def update(self, db: Session, db_brand: Brand, update_data: dict):
        for field, value in update_data.items():
            setattr(db_brand, field, value)
        db.commit()
        db.refresh(db_brand)
        return db_brand

    def get_by_id(self, db: Session, brand_id: int):
        return db.query(Brand).filter(Brand.id == brand_id).first()

    def delete(self, db: Session, db_brand: Brand):
        db.delete(db_brand)
        db.commit()
        return True
