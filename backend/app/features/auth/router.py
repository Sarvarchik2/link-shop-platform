from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
import uuid
from datetime import datetime, timedelta
from app.db.session import get_db
from app.core.config import settings
from app.core.security import create_access_token, get_password_hash
from app.features.users.service import UserService
from app.features.users.schemas import UserCreate, UserRead, Token, PasswordResetRequest, PasswordResetConfirm
from app.core.dependencies import get_current_user
from app.core.email import send_password_reset_email

router = APIRouter()
user_service = UserService()

@router.post("/password-reset/request")
def request_password_reset(request: PasswordResetRequest, db: Session = Depends(get_db)):
    user = user_service.get_user_by_email(db, request.email)
    if not user:
        # For security reasons, don't reveal if user exists, but here the PRD says something else.
        # Actually PRD says: IF user.is_email_verified == false: Return error.
        # So we must reveal if user exists or at least if email is verified.
        raise HTTPException(status_code=404, detail="Account with this email not found")
    
    if not user.is_email_verified:
        raise HTTPException(
            status_code=400, 
            detail="Сброс пароля невозможен. Ваша почта не была подтверждена в профиле"
        )
    
    # Generate token
    token = str(uuid.uuid4())
    
    # Save token
    user_service.update_user(db, user, {
        "reset_password_token": token,
        "reset_password_expires_at": datetime.utcnow() + timedelta(hours=1)
    })
    
    # Send email
    if send_password_reset_email(request.email, token):
        return {"message": "Password reset link sent to your email"}
    else:
        raise HTTPException(status_code=500, detail="Failed to send email")

@router.post("/password-reset/confirm")
def confirm_password_reset(request: PasswordResetConfirm, db: Session = Depends(get_db)):
    user = user_service.get_user_by_reset_token(db, request.token)
    if not user:
        raise HTTPException(status_code=400, detail="Invalid or expired reset token")
    
    if user.reset_password_expires_at < datetime.utcnow():
        raise HTTPException(status_code=400, detail="Reset token expired")
    
    # Update password
    user_service.update_user(db, user, {
        "password_hash": get_password_hash(request.new_password),
        "reset_password_token": None,
        "reset_password_expires_at": None
    })
    
    return {"message": "Password successfully reset"}

@router.post("/token", response_model=Token)
async def login_for_access_token(
    db: Session = Depends(get_db), form_data: OAuth2PasswordRequestForm = Depends()
):
    user = user_service.authenticate(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect phone or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        subject=user.phone, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}

@router.post("/register", response_model=Token)
def register_user(user_in: UserCreate, db: Session = Depends(get_db)):
    db_user = user_service.get_user_by_phone(db, phone=user_in.phone)
    if db_user:
        raise HTTPException(
            status_code=400,
            detail="User with this phone already exists",
        )
    user = user_service.register_user(db, user_in=user_in)
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        subject=user.phone, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}

@router.get("/users/me", response_model=UserRead)
def read_users_me(current_user=Depends(get_current_user)):
    return current_user
