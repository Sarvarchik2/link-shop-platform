from sqlalchemy.orm import Session
from typing import List, Optional
from .models import User

class UserRepository:
    def get_by_phone(self, db: Session, phone: str):
        return db.query(User).filter(User.phone == phone).first()

    def get_by_id(self, db: Session, user_id: int):
        return db.query(User).filter(User.id == user_id).first()

    def get_all(self, db: Session, skip: int = 0, limit: int = 100) -> List[User]:
        return db.query(User).offset(skip).limit(limit).all()

    def create(self, db: Session, user_data: dict):
        db_user = User(**user_data)
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        return db_user

    def get_by_email(self, db: Session, email: str):
        return db.query(User).filter(User.email == email).first()

    def get_by_reset_token(self, db: Session, token: str):
        return db.query(User).filter(User.reset_password_token == token).first()

    def update(self, db: Session, db_user: User, update_data: dict):
        for field, value in update_data.items():
            setattr(db_user, field, value)
        db.commit()
        db.refresh(db_user)
        return db_user
