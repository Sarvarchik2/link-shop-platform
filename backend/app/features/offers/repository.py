from sqlalchemy.orm import Session
from typing import List, Optional
from .models import Offer
from .schemas import OfferCreate, OfferUpdate

class OfferRepository:
    def get_all(self, db: Session, active_only: bool = True) -> List[Offer]:
        q = db.query(Offer)
        if active_only:
            q = q.filter(Offer.is_active == True)
        return q.order_by(Offer.display_order).all()

    def get_by_id(self, db: Session, offer_id: int) -> Optional[Offer]:
        return db.query(Offer).filter(Offer.id == offer_id).first()

    def create(self, db: Session, offer_in: OfferCreate) -> Offer:
        db_offer = Offer(**offer_in.model_dump())
        db.add(db_offer)
        db.commit()
        db.refresh(db_offer)
        return db_offer

    def update(self, db: Session, db_offer: Offer, offer_in: OfferUpdate) -> Offer:
        offer_data = offer_in.model_dump(exclude_unset=True)
        for key, value in offer_data.items():
            setattr(db_offer, key, value)
        
        db.add(db_offer)
        db.commit()
        db.refresh(db_offer)
        return db_offer

    def delete(self, db: Session, db_offer: Offer) -> Offer:
        db.delete(db_offer)
        db.commit()
        return db_offer
