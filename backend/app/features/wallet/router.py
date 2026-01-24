from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.core.dependencies import get_current_user
from app.features.users.models import User
from app.features.shops.service import ShopService
from .service import WalletService
from .schemas import (
    WalletTopUpRequest,
    WalletBalanceResponse,
    WalletTopUpResponse,
    TransactionListResponse
)

router = APIRouter(prefix="/wallet", tags=["Wallet"])
shop_service = ShopService()


@router.get("/balance", response_model=WalletBalanceResponse)
def get_wallet_balance(
    shop_slug: str = Query(..., description="Shop slug"),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Получить баланс кошелька магазина
    """
    # Проверить что магазин принадлежит текущему пользователю
    shop = shop_service.get_shop_by_slug(db, shop_slug)
    if not shop:
        raise HTTPException(status_code=404, detail="Shop not found")
    
    if shop.owner_id != current_user.id and current_user.role != "platform_admin":
        raise HTTPException(status_code=403, detail="Not authorized")
    
    wallet_service = WalletService(db)
    return wallet_service.get_balance(shop.id)


@router.post("/topup", response_model=WalletTopUpResponse)
def top_up_wallet(
    request: WalletTopUpRequest,
    shop_slug: str = Query(..., description="Shop slug"),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Пополнить баланс кошелька (тестовый режим)
    
    В тестовом режиме деньги зачисляются мгновенно без реального платежного шлюза.
    """
    # Проверить что магазин принадлежит текущему пользователю
    shop = shop_service.get_shop_by_slug(db, shop_slug)
    if not shop:
        raise HTTPException(status_code=404, detail="Shop not found")
    
    if shop.owner_id != current_user.id and current_user.role != "platform_admin":
        raise HTTPException(status_code=403, detail="Not authorized")
    
    wallet_service = WalletService(db)
    return wallet_service.top_up(shop.id, request.amount)


@router.get("/transactions", response_model=TransactionListResponse)
def get_wallet_transactions(
    shop_slug: str = Query(..., description="Shop slug"),
    limit: int = Query(20, ge=1, le=100),
    offset: int = Query(0, ge=0),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Получить историю транзакций кошелька
    """
    # Проверить что магазин принадлежит текущему пользователю
    shop = shop_service.get_shop_by_slug(db, shop_slug)
    if not shop:
        raise HTTPException(status_code=404, detail="Shop not found")
    
    if shop.owner_id != current_user.id and current_user.role != "platform_admin":
        raise HTTPException(status_code=403, detail="Not authorized")
    
    wallet_service = WalletService(db)
    return wallet_service.get_transactions(shop.id, limit, offset)
