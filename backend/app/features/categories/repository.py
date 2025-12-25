from sqlalchemy.orm import Session
from .models import Category

class CategoryRepository:
    def get_all(self, db: Session, shop_id: int = None):
        q = db.query(Category)
        if shop_id:
            q = q.filter(Category.shop_id == shop_id)
        else:
            q = q.filter(Category.shop_id == None)
        return q.all()

    def get_by_id(self, db: Session, category_id: int):
        return db.query(Category).filter(Category.id == category_id).first()

    def create(self, db: Session, category_data: dict):
        db_category = Category(**category_data)
        db.add(db_category)
        db.commit()
        db.refresh(db_category)
        return db_category

    def update(self, db: Session, db_category: Category, update_data: dict):
        for field, value in update_data.items():
            setattr(db_category, field, value)
        db.commit()
        db.refresh(db_category)
        return db_category

    def delete(self, db: Session, db_category: Category):
        db.delete(db_category)
        db.commit()
        return True
