from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List
from app.db.session import get_db
from .service import OfferService
from .schemas import OfferRead

router = APIRouter()
offer_service = OfferService()

@router.get("/offers", response_model=List[OfferRead])
def get_offers(db: Session = Depends(get_db)):
    return offer_service.get_offers(db)
