from sqlalchemy.orm import Session
from typing import List, Optional
from .models import Offer

class OfferRepository:
    def get_all(self, db: Session, active_only: bool = True) -> List[Offer]:
        q = db.query(Offer)
        if active_only:
            q = q.filter(Offer.is_active == True)
        return q.order_by(Offer.display_order).all()

    def get_by_id(self, db: Session, offer_id: int) -> Optional[Offer]:
        return db.query(Offer).filter(Offer.id == offer_id).first()
