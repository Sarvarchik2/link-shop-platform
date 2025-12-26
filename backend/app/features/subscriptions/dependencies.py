from fastapi import HTTPException, Depends, status
from sqlalchemy.orm import Session
from datetime import datetime
from app.db.session import get_db
from app.core.dependencies import get_current_user
from app.features.shops.service import ShopService
from app.features.subscriptions.service import SubscriptionService

shop_service = ShopService()
subscription_service = SubscriptionService()

def check_shop_active(
    shop_slug: str,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """
    Dependency to check if a shop is active and has a valid subscription.
    """
    shop = shop_service.get_shop_by_slug(db, shop_slug)
    
    # Ownership/Admin check
    if shop.owner_id != current_user.id and current_user.role != "platform_admin":
        raise HTTPException(status_code=403, detail="Not authorized")

    if not shop.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, 
            detail="Shop is deactivated. Please contact support."
        )

    # Check expiration
    if shop.subscription_status == "active" and shop.subscription_expires_at:
         if shop.subscription_expires_at < datetime.utcnow():
             raise HTTPException(
                 status_code=status.HTTP_402_PAYMENT_REQUIRED,
                 detail="Subscription expired. Please renew your plan."
             )
    
    # Check trial expiration (if we treat 'trial' as a status that can expire based on created_at + period)
    # Ideally, logic handles transition to 'expired', but this is a safety net.
    if shop.subscription_status == "trial" and shop.subscription_expires_at:
        if shop.subscription_expires_at < datetime.utcnow():
             raise HTTPException(
                 status_code=status.HTTP_402_PAYMENT_REQUIRED,
                 detail="Trial period expired. Please choose a plan."
             )
             
    return shop

def check_product_limit(
    shop_slug: str,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """
    Dependency to check if shop has reached its product limit.
    Returns shop if limit not reached.
    """
    shop = check_shop_active(shop_slug, db, current_user)
    
    # If admin, bypass limits? Maybe not, strictly enforce plan limits unless special override.
    if current_user.role == "platform_admin":
        return shop

    if not shop.subscription_plan_id:
        # If no plan (shouldn't happen for valid shops, maybe legacy), assume restricted
        # Or look up "Trial" plan defaults.
        # For now, let's fetch the plan linked to the shop.
        pass

    # We need the plan details.
    # If we have a direct relation in models we could use shop.subscription_plan
    # But since we might not have lazy loading set up fully or correctly, let's fetch carefully.
    
    limit = 0
    if shop.subscription_plan_id:
        plan = subscription_service.get_plan(db, shop.subscription_plan_id)
        limit = plan.max_products
    else:
        # Fallback for trial if plan_id is null but status is trial?
        # Ideally all shops have a plan_id now.
        # Let's assume default trial limit if no plan
        limit = 50 # Hardcoded fallback or fetch "trial" plan
    
    if limit is None: # None means unlimited
        return shop
        
    current_count = shop_service.get_shop_stats(db, shop.slug, current_user).total_products
    
    if current_count >= limit:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=f"Product limit reached for your plan ({limit} products). Upgrade your plan to add more."
        )
        
    return shop
