from fastapi import APIRouter, Depends, Query, HTTPException
from sqlalchemy.orm import Session
from typing import List, Optional
from app.db.session import get_db
from app.core.dependencies import get_current_user
from .service import BrandService
from pydantic import BaseModel

class BrandSchema(BaseModel):
    id: Optional[int] = None
    name: str
    logo_url: str
    shop_id: Optional[int] = None
    class Config:
        from_attributes = True

class BrandCreate(BaseModel):
    name: str
    logo_url: str

class BrandUpdate(BaseModel):
    name: Optional[str] = None
    logo_url: Optional[str] = None

router = APIRouter()
brand_service = BrandService()

@router.get("/brands", response_model=List[BrandSchema])
def get_brands(shop_slug: Optional[str] = Query(None), db: Session = Depends(get_db)):
    return brand_service.get_brands(db, shop_slug=shop_slug)

@router.post("/brands", response_model=BrandSchema)
def create_brand(
    brand_in: BrandCreate, 
    shop_slug: Optional[str] = Query(None), 
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    return brand_service.create_brand(db, brand_in, shop_slug, current_user)

@router.put("/brands/{brand_id}", response_model=BrandSchema)
def update_brand(
    brand_id: int,
    brand_in: BrandUpdate,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    return brand_service.update_brand(db, brand_id, brand_in, current_user)

@router.delete("/brands/{brand_id}")
def delete_brand(
    brand_id: int,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    return brand_service.delete_brand(db, brand_id, current_user)
