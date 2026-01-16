from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.db.session import get_db
from app.core.dependencies import get_current_user, get_current_platform_admin
import random
from datetime import datetime, timedelta
from .schemas import UserRead, EmailLinkRequest, EmailVerifyRequest, UserUpdate
from .service import UserService
from app.core.email import send_verification_code
from .models import User

router = APIRouter()
user_service = UserService()

@router.get("/users/me", response_model=UserRead)
def read_users_me(current_user: User = Depends(get_current_user)):
    return current_user

@router.put("/users/profile", response_model=UserRead)
def update_profile(
    user_update: UserUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    update_data = user_update.dict(exclude_unset=True)
    
    # If email is being updated and it's different from current, reset verification
    if "email" in update_data and update_data["email"] != current_user.email:
        update_data["is_email_verified"] = False
        
    return user_service.update_user(db, current_user, update_data)

@router.post("/settings/email/link")
def link_email(
    request: EmailLinkRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    # Check if email is already verified by another user
    existing_user = user_service.get_user_by_email(db, request.email)
    if existing_user and existing_user.is_email_verified and existing_user.id != current_user.id:
        raise HTTPException(status_code=400, detail="This email is already verified by another account")
    
    # Generate 6-digit code
    code = f"{random.randint(100000, 999999)}"
    
    # Save to user
    user_service.update_user(db, current_user, {
        "email": request.email,
        "email_verification_code": code,
        "verification_expires_at": datetime.utcnow() + timedelta(minutes=15)
    })
    
    # Send email
    if send_verification_code(request.email, code):
        return {"message": "Verification code sent to your email"}
    else:
        raise HTTPException(status_code=500, detail="Failed to send email")

@router.post("/settings/email/verify")
def verify_email(
    request: EmailVerifyRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    if not current_user.email_verification_code:
        raise HTTPException(status_code=400, detail="No verification code found")
    
    if current_user.verification_expires_at < datetime.utcnow():
        raise HTTPException(status_code=400, detail="Verification code expired")
    
    if current_user.email_verification_code != request.code:
        raise HTTPException(status_code=400, detail="Invalid verification code")
    
    # Mark as verified
    user_service.update_user(db, current_user, {
        "is_email_verified": True,
        "email_verification_code": None,
        "verification_expires_at": None
    })
    
    return {"message": "Email successfully verified"}

@router.get("/platform/admin/users", response_model=List[UserRead])
def read_all_users(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    admin: UserRead = Depends(get_current_platform_admin)
):
    """
    Get all users. Only for platform administrators.
    """
    return user_service.get_all_users(db, skip=skip, limit=limit)
