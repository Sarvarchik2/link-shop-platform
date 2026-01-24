from sqlalchemy import Column, Integer, String, DateTime, Numeric, ForeignKey, JSON
from datetime import datetime
from app.db.base_class import Base

class Wallet(Base):
    """Кошелек магазина для оплаты подписок"""
    __tablename__ = "wallet"
    
    id = Column(Integer, primary_key=True, index=True)
    shop_id = Column(Integer, ForeignKey("shop.id"), unique=True, nullable=False, index=True)
    balance = Column(Numeric(15, 2), default=0.00, nullable=False)
    currency = Column(String, default="UZS", nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)


class Transaction(Base):
    """История транзакций кошелька"""
    __tablename__ = "transaction"
    
    id = Column(Integer, primary_key=True, index=True)
    wallet_id = Column(Integer, ForeignKey("wallet.id"), nullable=False, index=True)
    type = Column(String, nullable=False)  # TOPUP, PAYMENT, REFUND
    amount = Column(Numeric(15, 2), nullable=False)
    description = Column(String, nullable=True)
    status = Column(String, default="PENDING", nullable=False)  # PENDING, COMPLETED, FAILED
    meta_data = Column(JSON, nullable=True)  # payment_method, subscription_id, etc.
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

