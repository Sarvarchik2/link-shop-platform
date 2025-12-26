from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List
from app.db.session import get_db
from app.core.dependencies import get_current_platform_admin
from .service import OfferService
from .schemas import OfferRead, OfferCreate, OfferUpdate

router = APIRouter()
offer_service = OfferService()

@router.get("/offers", response_model=List[OfferRead])
def get_public_offers(db: Session = Depends(get_db)):
    """Public endpoint to get active offers"""
    return offer_service.get_offers(db, active_only=True)

@router.get("/platform/admin/offers", response_model=List[OfferRead])
def get_admin_offers(
    db: Session = Depends(get_db),
    admin = Depends(get_current_platform_admin)
):
    """Admin endpoint to get all offers (including inactive)"""
    return offer_service.get_offers(db, active_only=False)

@router.post("/platform/admin/offers", response_model=OfferRead)
def create_offer(
    offer_in: OfferCreate,
    db: Session = Depends(get_db),
    admin = Depends(get_current_platform_admin)
):
    return offer_service.create_offer(db, offer_in)

@router.put("/platform/admin/offers/{offer_id}", response_model=OfferRead)
def update_offer(
    offer_id: int,
    offer_in: OfferUpdate,
    db: Session = Depends(get_db),
    admin = Depends(get_current_platform_admin)
):
    return offer_service.update_offer(db, offer_id, offer_in)

@router.delete("/platform/admin/offers/{offer_id}", response_model=OfferRead)
def delete_offer(
    offer_id: int,
    db: Session = Depends(get_db),
    admin = Depends(get_current_platform_admin)
):
    return offer_service.delete_offer(db, offer_id)
