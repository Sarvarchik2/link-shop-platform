from fastapi import APIRouter, Depends, Query, HTTPException
from sqlalchemy.orm import Session
from typing import List, Optional
from app.db.session import get_db
from app.core.dependencies import get_current_user
from .service import CategoryService
from pydantic import BaseModel

class CategorySchema(BaseModel):
    id: Optional[int] = None
    name: str
    image_url: Optional[str] = None
    shop_id: Optional[int] = None
    class Config:
        from_attributes = True

class CategoryCreate(BaseModel):
    name: str
    image_url: Optional[str] = None

class CategoryUpdate(BaseModel):
    name: Optional[str] = None
    image_url: Optional[str] = None

router = APIRouter()
category_service = CategoryService()

@router.get("/categories", response_model=List[CategorySchema])
def get_categories(shop_slug: Optional[str] = Query(None), db: Session = Depends(get_db)):
    return category_service.get_categories(db, shop_slug=shop_slug)

@router.post("/categories", response_model=CategorySchema)
def create_category(
    category_in: CategoryCreate, 
    shop_slug: Optional[str] = Query(None), 
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    return category_service.create_category(db, category_in, shop_slug, current_user)

@router.put("/categories/{category_id}", response_model=CategorySchema)
def update_category(
    category_id: int,
    category_in: CategoryUpdate,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    return category_service.update_category(db, category_id, category_in, current_user)

@router.delete("/categories/{category_id}")
def delete_category(
    category_id: int,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    return category_service.delete_category(db, category_id, current_user)
