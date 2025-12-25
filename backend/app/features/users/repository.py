from sqlalchemy.orm import Session
from .models import User

class UserRepository:
    def get_by_phone(self, db: Session, phone: str):
        return db.query(User).filter(User.phone == phone).first()

    def get_by_id(self, db: Session, user_id: int):
        return db.query(User).filter(User.id == user_id).first()

    def create(self, db: Session, user_data: dict):
        db_user = User(**user_data)
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        return db_user

    def update(self, db: Session, db_user: User, update_data: dict):
        for field, value in update_data.items():
            setattr(db_user, field, value)
        db.commit()
        db.refresh(db_user)
        return db_user
