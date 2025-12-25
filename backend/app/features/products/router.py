from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from app.db.session import get_db
from app.core.dependencies import get_current_user
from .service import ProductService
from .schemas import ProductCreate, ProductRead, ProductUpdate

router = APIRouter()
product_service = ProductService()

@router.get("/products", response_model=List[ProductRead])
def get_products(
    db: Session = Depends(get_db),
    skip: int = 0,
    limit: int = 100,
    shop_id: Optional[int] = None,
    shop_slug: Optional[str] = None,
    category: Optional[str] = None,
    brand: Optional[str] = None,
    q: Optional[str] = None
):
    return product_service.get_products(
        db, skip=skip, limit=limit, shop_id=shop_id, shop_slug=shop_slug, category=category, brand=brand, query=q
    )

@router.get("/products/{product_id}", response_model=ProductRead)
def get_product(product_id: int, db: Session = Depends(get_db)):
    return product_service.get_product(db, product_id)

@router.post("/products", response_model=ProductRead)
def create_product(
    product_in: ProductCreate,
    shop_slug: Optional[str] = Query(None),
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    return product_service.create_product(db, product_in, shop_slug, current_user)

@router.put("/products/{product_id}", response_model=ProductRead)
def update_product(
    product_id: int,
    product_in: ProductUpdate,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    return product_service.update_product(db, product_id, product_in, current_user)

@router.delete("/products/{product_id}")
def delete_product(
    product_id: int,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    return product_service.delete_product(db, product_id, current_user)
