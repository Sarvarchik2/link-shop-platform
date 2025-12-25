from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from sqlalchemy.orm import Session
from app.core.config import settings
from app.db.session import get_db
from app.features.users.service import UserService
from app.features.users.schemas import TokenData

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
user_service = UserService()

async def get_current_user(
    db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)
):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(
            token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM]
        )
        phone: str = payload.get("sub")
        if phone is None:
            raise credentials_exception
        token_data = TokenData(phone=phone)
    except JWTError:
        raise credentials_exception
    
    user = user_service.get_user_by_phone(db, phone=token_data.phone)
    if user is None:
        raise credentials_exception
    return user

async def get_current_admin(current_user=Depends(get_current_user)):
    if current_user.role not in ["admin", "platform_admin"]:
        raise HTTPException(status_code=403, detail="Not authorized")
    return current_user

async def get_current_platform_admin(current_user=Depends(get_current_user)):
    if current_user.role != "platform_admin":
        raise HTTPException(status_code=403, detail="Not authorized")
    return current_user
