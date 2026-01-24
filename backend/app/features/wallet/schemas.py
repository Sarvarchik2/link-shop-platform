from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional, List
from decimal import Decimal

# Request Schemas
class WalletTopUpRequest(BaseModel):
    amount: Decimal = Field(..., gt=0, description="Сумма пополнения")

class WalletBalanceResponse(BaseModel):
    balance: Decimal
    currency: str

class TransactionResponse(BaseModel):
    id: int
    type: str
    amount: Decimal
    description: Optional[str]
    status: str
    created_at: datetime
    
    class Config:
        from_attributes = True

class TransactionListResponse(BaseModel):
    transactions: List[TransactionResponse]
    total: int

class WalletTopUpResponse(BaseModel):
    success: bool
    new_balance: Decimal
    transaction_id: int
    message: str = "Баланс успешно пополнен"
