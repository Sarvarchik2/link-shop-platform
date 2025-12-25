from fastapi import APIRouter, Depends, Query, HTTPException
from sqlalchemy.orm import Session
from typing import List, Optional
from app.db.session import get_db
from app.core.dependencies import get_current_user
from .service import BannerService
from pydantic import BaseModel

class BannerSchema(BaseModel):
    id: Optional[int] = None
    badge_text: str
    title: str
    subtitle: str
    button_text: str
    button_link: str
    image_url: str
    is_active: bool
    shop_id: Optional[int] = None
    
    class Config:
        from_attributes = True

class BannerCreate(BaseModel):
    badge_text: str
    title: str
    subtitle: str
    button_text: str
    button_link: str
    image_url: str
    is_active: bool

router = APIRouter()
banner_service = BannerService()

@router.get("/banner", response_model=List[BannerSchema])
def get_banners(shop_slug: Optional[str] = Query(None), db: Session = Depends(get_db)):
    return banner_service.get_banners(db, shop_slug=shop_slug)

@router.put("/banner", response_model=BannerSchema)
def update_banner(
    banner_in: BannerCreate,
    shop_slug: Optional[str] = Query(None),
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    return banner_service.update_banner(db, banner_in, shop_slug, current_user)
