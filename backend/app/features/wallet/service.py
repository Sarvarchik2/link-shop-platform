from sqlalchemy.orm import Session
from decimal import Decimal
from typing import Optional, Tuple, List
from .repository import WalletRepository, TransactionRepository
from .models import Wallet, Transaction
from .schemas import WalletBalanceResponse, WalletTopUpResponse, TransactionResponse, TransactionListResponse

class WalletService:
    """Сервис для работы с кошельком"""
    
    def __init__(self, db: Session):
        self.db = db
        self.wallet_repo = WalletRepository(db)
        self.transaction_repo = TransactionRepository(db)
    
    def get_balance(self, shop_id: int) -> WalletBalanceResponse:
        """Получить баланс кошелька магазина"""
        wallet = self.wallet_repo.get_or_create(shop_id)
        return WalletBalanceResponse(
            balance=wallet.balance,
            currency=wallet.currency
        )
    
    def top_up(self, shop_id: int, amount: Decimal) -> WalletTopUpResponse:
        """Пополнить кошелек (тестовый режим)"""
        # Получить или создать кошелек
        wallet = self.wallet_repo.get_or_create(shop_id)
        
        # Создать транзакцию
        transaction = self.transaction_repo.create(
            wallet_id=wallet.id,
            type="TOPUP",
            amount=amount,
            description=f"Пополнение баланса (тестовый режим)",
            status="COMPLETED",
            meta_data={"payment_method": "test"}
        )
        
        # Обновить баланс
        wallet = self.wallet_repo.update_balance(wallet.id, amount)
        
        return WalletTopUpResponse(
            success=True,
            new_balance=wallet.balance,
            transaction_id=transaction.id
        )
    
    def get_transactions(
        self,
        shop_id: int,
        limit: int = 20,
        offset: int = 0
    ) -> TransactionListResponse:
        """Получить историю транзакций"""
        wallet = self.wallet_repo.get_or_create(shop_id)
        transactions, total = self.transaction_repo.get_by_wallet(
            wallet_id=wallet.id,
            limit=limit,
            offset=offset
        )
        
        return TransactionListResponse(
            transactions=[TransactionResponse.from_orm(t) for t in transactions],
            total=total
        )
    
    def charge(
        self,
        shop_id: int,
        amount: Decimal,
        description: str,
        meta_data: dict = None
    ) -> Tuple[bool, Optional[Transaction]]:
        """Списать средства с кошелька"""
        wallet = self.wallet_repo.get_or_create(shop_id)
        
        # Проверить достаточность средств
        if wallet.balance < amount:
            return False, None
        
        # Создать транзакцию списания
        transaction = self.transaction_repo.create(
            wallet_id=wallet.id,
            type="PAYMENT",
            amount=-amount,  # Отрицательная сумма для списания
            description=description,
            status="COMPLETED",
            meta_data=meta_data or {}
        )
        
        # Обновить баланс
        self.wallet_repo.update_balance(wallet.id, -amount)
        
        return True, transaction

    
    def has_sufficient_balance(self, shop_id: int, amount: Decimal) -> bool:
        """Проверить достаточность средств"""
        wallet = self.wallet_repo.get_or_create(shop_id)
        return wallet.balance >= amount
