from fastapi import APIRouter, Depends, Request, HTTPException
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.features.shops.models import Shop, UserStoreTelegram
from app.features.users.models import User
import logging

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/telegram", tags=["telegram"])


@router.post("/webhook/{shop_slug}")
async def telegram_webhook(
    shop_slug: str,
    request: Request,
    db: Session = Depends(get_db)
):
    """
    Telegram webhook endpoint for receiving updates from bot.
    URL format: https://your-app.railway.app/telegram/webhook/{shop_slug}
    """
    try:
        # Get shop and verify bot is active
        shop = db.query(Shop).filter(Shop.slug == shop_slug).first()
        if not shop or not shop.telegram_bot_token or not shop.is_bot_active:
            logger.warning(f"Webhook called for invalid/inactive shop: {shop_slug}")
            return {"ok": True}  # Return ok to Telegram to avoid retries
        
        # Parse Telegram update
        update = await request.json()
        logger.info(f"Received webhook update for {shop_slug}: {update}")
        
        # Handle different update types
        if "message" in update:
            await handle_message(update["message"], shop, db)
        elif "callback_query" in update:
            await handle_callback_query(update["callback_query"], shop, db)
        
        return {"ok": True}
        
    except Exception as e:
        logger.error(f"Error processing webhook: {e}", exc_info=True)
        return {"ok": True}  # Return ok anyway to avoid Telegram retries


async def handle_message(message: dict, shop: Shop, db: Session):
    """Handle incoming messages"""
    try:
        chat_id = message["chat"]["id"]
        text = message.get("text", "")
        telegram_user = message.get("from", {})
        
        logger.info(f"Message from {chat_id}: {text}")
        
        # Handle /start command
        if text.startswith("/start"):
            await handle_start_command(chat_id, telegram_user, shop, db)
        
    except Exception as e:
        logger.error(f"Error handling message: {e}", exc_info=True)


async def handle_start_command(chat_id: int, telegram_user: dict, shop: Shop, db: Session):
    """
    Handle /start command - register user for broadcasts
    """
    try:
        # Get Telegram user info
        telegram_id = telegram_user.get("id")
        telegram_username = telegram_user.get("username")
        first_name = telegram_user.get("first_name", "")
        last_name = telegram_user.get("last_name", "")
        
        logger.info(f"Start command from: {telegram_username} (ID: {telegram_id})")
        
        # Try to find existing user by telegram username or phone
        # For now, we'll create a guest user or link to existing
        user = None
        
        # Option 1: Try to find by phone if telegram has phone
        # Note: Telegram API doesn't share phone in messages, only in auth
        
        # Option 2: Create a guest user for this telegram account
        # Check if already registered
        existing_mapping = db.query(UserStoreTelegram).filter(
            UserStoreTelegram.store_id == shop.id,
            UserStoreTelegram.telegram_chat_id == str(chat_id)
        ).first()
        
        if existing_mapping:
            logger.info(f"User already registered for broadcasts: {chat_id}")
            # Send confirmation message
            await send_telegram_message(
                shop.telegram_bot_token,
                chat_id,
                f"✅ Вы уже подписаны на уведомления от {shop.name}!"
            )
            return
        
        # Find or create user
        # For simplicity, we'll use a general "telegram_subscribers" user
        # Or create specific user per telegram account
        telegram_display_name = f"{first_name} {last_name}".strip() or telegram_username or f"User{telegram_id}"
        
        # Check if user exists with this telegram_id in any shop
        user_mapping = db.query(UserStoreTelegram).filter(
            UserStoreTelegram.telegram_chat_id == str(chat_id)
        ).first()
        
        if user_mapping:
            # User exists in another shop, link to same user
            user_id = user_mapping.user_id
        else:
            # Create new user for this telegram account
            # Use telegram_id as phone (temporary)
            user = User(
                phone=f"+tg{telegram_id}",  # Temporary phone
                password_hash="",  # No password for telegram users
                first_name=first_name or "Telegram",
                last_name=last_name or "User"
            )
            db.add(user)
            db.flush()
            user_id = user.id
        
        # Create mapping
        mapping = UserStoreTelegram(
            user_id=user_id,
            store_id=shop.id,
            telegram_chat_id=str(chat_id)
        )
        db.add(mapping)
        db.commit()
        
        logger.info(f"Registered user {user_id} for broadcasts in shop {shop.id}")
        
        # Send welcome message
        await send_telegram_message(
            shop.telegram_bot_token,
            chat_id,
            f"🎉 Добро пожаловать в {shop.name}!\n\n"
            f"✅ Вы подписаны на уведомления:\n"
            f"• Обновления статуса заказов\n"
            f"• Новости и акции\n"
            f"• Специальные предложения\n\n"
            f"Открыть магазин: https://storely.uz/s/{shop.slug}"
        )
        
    except Exception as e:
        logger.error(f"Error in start command: {e}", exc_info=True)
        db.rollback()


async def handle_callback_query(callback_query: dict, shop: Shop, db: Session):
    """Handle callback queries from inline buttons"""
    # Future: handle unsubscribe, etc.
    pass


async def send_telegram_message(bot_token: str, chat_id: int, text: str):
    """Send a message via Telegram Bot API"""
    import httpx
    
    try:
        url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
        payload = {
            "chat_id": chat_id,
            "text": text,
            "parse_mode": "HTML"
        }
        
        async with httpx.AsyncClient() as client:
            response = await client.post(url, json=payload)
            if response.status_code != 200:
                logger.error(f"Failed to send message: {response.text}")
            else:
                logger.info(f"Message sent to {chat_id}")
    except Exception as e:
        logger.error(f"Error sending telegram message: {e}")
