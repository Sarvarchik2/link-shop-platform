from sqlalchemy.orm import Session
from typing import List, Optional
from fastapi import HTTPException, status
from .repository import OfferRepository
from .schemas import OfferCreate, OfferUpdate

class OfferService:
    def __init__(self):
        self.repository = OfferRepository()

    def get_offers(self, db: Session, active_only: bool = True):
        return self.repository.get_all(db, active_only)

    def get_offer(self, db: Session, offer_id: int):
        offer = self.repository.get_by_id(db, offer_id)
        if not offer:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Offer not found"
            )
        return offer

    def create_offer(self, db: Session, offer_in: OfferCreate):
        return self.repository.create(db, offer_in)

    def update_offer(self, db: Session, offer_id: int, offer_in: OfferUpdate):
        offer = self.get_offer(db, offer_id)
        return self.repository.update(db, offer, offer_in)

    def delete_offer(self, db: Session, offer_id: int):
        offer = self.get_offer(db, offer_id)
        return self.repository.delete(db, offer)
