from sqlalchemy.orm import Session
from .repository import UserRepository
from .schemas import UserCreate
from app.core.security import get_password_hash, verify_password

class UserService:
    def __init__(self):
        self.repository = UserRepository()

    def get_user_by_phone(self, db: Session, phone: str):
        return self.repository.get_by_phone(db, phone)

    def register_user(self, db: Session, user_in: UserCreate):
        user_data = user_in.model_dump()
        password = user_data.pop("password")
        user_data["password_hash"] = get_password_hash(password)
        return self.repository.create(db, user_data)

    def authenticate(self, db: Session, phone, password):
        user = self.repository.get_by_phone(db, phone)
        if not user:
            return None
        if not verify_password(password, user.password_hash):
            return None
        return user

    def update_role(self, db: Session, user_id: int, role: str):
        user = self.repository.get_by_id(db, user_id)
        if user:
            return self.repository.update(db, user, {"role": role})
        return None
