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
    
    title_ru: Optional[str] = None
    title_en: Optional[str] = None
    title_uz: Optional[str] = None
    title: str # Fallback/Primary

    subtitle_ru: Optional[str] = None
    subtitle_en: Optional[str] = None
    subtitle_uz: Optional[str] = None
    subtitle: str

    button_text_ru: Optional[str] = None
    button_text_en: Optional[str] = None
    button_text_uz: Optional[str] = None
    button_text: str

    button_link: str
    image_url: str
    is_active: bool
    shop_id: Optional[int] = None
    
    class Config:
        from_attributes = True

class BannerCreate(BaseModel):
    badge_text: Optional[str] = None
    
    title_ru: Optional[str] = None
    title_en: Optional[str] = None
    title_uz: Optional[str] = None
    title: str

    subtitle_ru: Optional[str] = None
    subtitle_en: Optional[str] = None
    subtitle_uz: Optional[str] = None
    subtitle: str

    button_text_ru: Optional[str] = None
    button_text_en: Optional[str] = None
    button_text_uz: Optional[str] = None
    button_text: str

    button_link: str
    image_url: str
    is_active: bool = True

router = APIRouter()
banner_service = BannerService()

@router.get("/banner", response_model=List[BannerSchema])
def get_banners(shop_slug: Optional[str] = Query(None), db: Session = Depends(get_db)):
    return banner_service.get_banners(db, shop_slug=shop_slug)

@router.get("/banner/{banner_id}", response_model=BannerSchema)
def get_banner(
    banner_id: int,
    shop_slug: str = Query(...),
    db: Session = Depends(get_db)
):
    return banner_service.get_banner_public(db, banner_id, shop_slug)

@router.post("/banner", response_model=BannerSchema)
def create_banner(
    banner_in: BannerCreate,
    shop_slug: str = Query(...),
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    return banner_service.create_banner(db, banner_in, shop_slug, current_user)

@router.put("/banner/{banner_id}", response_model=BannerSchema)
def update_banner(
    banner_id: int,
    banner_in: BannerCreate,
    shop_slug: str = Query(...),
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    return banner_service.update_banner(db, banner_id, banner_in, shop_slug, current_user)

@router.delete("/banner/{banner_id}")
def delete_banner(
    banner_id: int,
    shop_slug: str = Query(...),
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    banner_service.delete_banner(db, banner_id, shop_slug, current_user)
    return {"message": "Banner deleted"}

