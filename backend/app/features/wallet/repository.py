from sqlalchemy.orm import Session
from sqlalchemy import desc
from typing import Optional, List
from decimal import Decimal
from .models import Wallet, Transaction

class WalletRepository:
    """Repository для работы с кошельками"""
    
    def __init__(self, db: Session):
        self.db = db
    
    def get_by_shop_id(self, shop_id: int) -> Optional[Wallet]:
        """Получить кошелек магазина"""
        return self.db.query(Wallet).filter(Wallet.shop_id == shop_id).first()
    
    def create(self, shop_id: int) -> Wallet:
        """Создать кошелек для магазина"""
        wallet = Wallet(shop_id=shop_id, balance=0.00, currency="UZS")
        self.db.add(wallet)
        self.db.commit()
        self.db.refresh(wallet)
        return wallet
    
    def get_or_create(self, shop_id: int) -> Wallet:
        """Получить или создать кошелек"""
        wallet = self.get_by_shop_id(shop_id)
        if not wallet:
            wallet = self.create(shop_id)
        return wallet
    
    def update_balance(self, wallet_id: int, amount: Decimal) -> Wallet:
        """Обновить баланс кошелька"""
        wallet = self.db.query(Wallet).filter(Wallet.id == wallet_id).first()
        if wallet:
            wallet.balance += amount
            self.db.commit()
            self.db.refresh(wallet)
        return wallet


class TransactionRepository:
    """Repository для работы с транзакциями"""
    
    def __init__(self, db: Session):
        self.db = db
    
    def create(
        self,
        wallet_id: int,
        type: str,
        amount: Decimal,
        description: str = None,
        status: str = "COMPLETED",
        meta_data: dict = None
    ) -> Transaction:
        """Создать транзакцию"""
        transaction = Transaction(
            wallet_id=wallet_id,
            type=type,
            amount=amount,
            description=description,
            status=status,
            meta_data=meta_data or {}
        )
        self.db.add(transaction)
        self.db.commit()
        self.db.refresh(transaction)
        return transaction

    
    def get_by_wallet(
        self,
        wallet_id: int,
        limit: int = 20,
        offset: int = 0
    ) -> tuple[List[Transaction], int]:
        """Получить транзакции кошелька с пагинацией"""
        query = self.db.query(Transaction).filter(Transaction.wallet_id == wallet_id)
        total = query.count()
        transactions = query.order_by(desc(Transaction.created_at)).limit(limit).offset(offset).all()
        return transactions, total
    
    def get_by_id(self, transaction_id: int) -> Optional[Transaction]:
        """Получить транзакцию по ID"""
        return self.db.query(Transaction).filter(Transaction.id == transaction_id).first()

    def get_all(
        self,
        limit: int = 20,
        offset: int = 0
    ) -> tuple[List[Transaction], int]:
        """Получить все транзакции системы с пагинацией"""
        query = self.db.query(Transaction)
        total = query.count()
        transactions = query.order_by(desc(Transaction.created_at)).limit(limit).offset(offset).all()
        return transactions, total
