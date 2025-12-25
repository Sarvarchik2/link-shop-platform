from sqlalchemy.orm import Session
from .models import Shop
from app.features.users.models import User

class ShopRepository:
    def get_by_slug(self, db: Session, slug: str):
        return db.query(Shop).filter(Shop.slug == slug).first()

    def get_by_id(self, db: Session, shop_id: int):
        return db.query(Shop).filter(Shop.id == shop_id).first()

    def get_by_owner_id(self, db: Session, owner_id: int):
        return db.query(Shop).filter(Shop.owner_id == owner_id).first()

    def get_all(self, db: Session):
        return db.query(Shop).all()

    def get_all_with_owners(self, db: Session):
        return db.query(Shop, User.first_name, User.last_name, User.phone).\
            join(User, Shop.owner_id == User.id).all()

    def create(self, db: Session, shop_data: dict):
        db_shop = Shop(**shop_data)
        db.add(db_shop)
        db.commit()
        db.refresh(db_shop)
        return db_shop

    def update(self, db: Session, db_shop: Shop, update_data: dict):
        for field, value in update_data.items():
            setattr(db_shop, field, value)
        db.commit()
        db.refresh(db_shop)
        return db_shop
