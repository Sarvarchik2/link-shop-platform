from sqlalchemy.orm import Session
from .repository import OfferRepository

class OfferService:
    def __init__(self):
        self.repository = OfferRepository()

    def get_offers(self, db: Session, active_only: bool = True):
        return self.repository.get_all(db, active_only)
