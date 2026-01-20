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
    Handle /start command - register user for broadcasts and ask for language
    """
    try:
        # Get Telegram user info
        telegram_id = telegram_user.get("id")
        first_name = telegram_user.get("first_name", "")
        last_name = telegram_user.get("last_name", "")
        
        # Find or create user
        mapping = db.query(UserStoreTelegram).filter(
            UserStoreTelegram.store_id == shop.id,
            UserStoreTelegram.telegram_chat_id == str(chat_id)
        ).first()
        
        if not mapping:
            # Check if user exists with this telegram_id in any shop
            user_mapping = db.query(UserStoreTelegram).filter(
                UserStoreTelegram.telegram_chat_id == str(chat_id)
            ).first()
            
            if user_mapping:
                user_id = user_mapping.user_id
            else:
                user = User(
                    phone=f"+tg{telegram_id}",
                    password_hash="",
                    first_name=first_name or "Telegram",
                    last_name=last_name or "User"
                )
                db.add(user)
                db.flush()
                user_id = user.id
            
            mapping = UserStoreTelegram(
                user_id=user_id,
                store_id=shop.id,
                telegram_chat_id=str(chat_id),
                language="ru" # Default
            )
            db.add(mapping)
            db.commit()
            logger.info(f"✅ Registered user {user_id} for shop {shop.id}")

        # Send language selection menu
        keyboard = {
            "inline_keyboard": [
                [
                    {"text": "🇷🇺 Русский", "callback_data": "lang_ru"},
                    {"text": "🇺🇿 O'zbekcha", "callback_data": "lang_uz"},
                    {"text": "🇺🇸 English", "callback_data": "lang_en"}
                ]
            ]
        }
        
        await send_telegram_message(
            shop.telegram_bot_token,
            chat_id,
            f"👋 <b>Welcome to {shop.name}!</b>\n\n"
            f"Please choose your preferred language for notifications:\n"
            f"Пожалуйста, выберите удобный язык для уведомлений:\n"
            f"Iltimos, xabarnomalar uchun qulay tilni tanlang:",
            reply_markup=keyboard
        )
        
    except Exception as e:
        logger.error(f"Error in start command: {e}", exc_info=True)
        db.rollback()


async def handle_callback_query(callback_query: dict, shop: Shop, db: Session):
    """Handle callback queries from inline buttons"""
    try:
        chat_id = callback_query["message"]["chat"]["id"]
        data = callback_query.get("data", "")
        message_id = callback_query["message"]["message_id"]

        if data.startswith("lang_"):
            lang = data.split("_")[1]
            # Update user language
            mapping = db.query(UserStoreTelegram).filter(
                UserStoreTelegram.store_id == shop.id,
                UserStoreTelegram.telegram_chat_id == str(chat_id)
            ).first()
            
            if mapping:
                mapping.language = lang
                db.commit()
                
                # Answer callback
                await answer_callback_query(shop.telegram_bot_token, callback_query["id"], "Success!")
                
                # Delete choosing language message to keep chat clean
                await delete_telegram_message(shop.telegram_bot_token, chat_id, message_id)
                
                # Prepare beautiful welcome message
                shop_url = f"https://storely.uz/{shop.slug}"
                
                # Contacts block
                contacts = []
                if shop.phone: contacts.append(f"📞 {shop.phone}")
                if shop.email: contacts.append(f"📧 {shop.email}")
                if shop.address: contacts.append(f"📍 {shop.address}")
                
                socials = []
                if shop.instagram: socials.append(f"<a href='https://instagram.com/{shop.instagram.strip('@')}'>Instagram</a>")
                if shop.telegram: socials.append(f"<a href='https://t.me/{shop.telegram.strip('@')}'>Telegram</a>")
                if shop.facebook: socials.append(f"<a href='{shop.facebook}'>Facebook</a>")
                if shop.twitter: socials.append(f"<a href='https://twitter.com/{shop.twitter.strip('@')}'>Twitter</a>")
                if shop.whatsapp: 
                    wa_phone = shop.whatsapp.strip('+').replace(' ', '')
                    socials.append(f"<a href='https://wa.me/{wa_phone}'>WhatsApp</a>")
                
                contacts_str = "\n".join(contacts)
                socials_str = " | ".join(socials)
                
                welcome_data = {
                    "ru": {
                        "text": f"🎉 <b>Добро пожаловать в {shop.name}!</b>\n\n"
                                f"Мы рады видеть вас в нашем магазине. Теперь вы будете получать уведомления о статусе ваших заказов и специальных предложениях.\n\n"
                                f"{'<b>Контакты:</b>' if contacts_str else ''}\n{contacts_str}\n\n"
                                f"{'<b>Мы в соцсетях:</b>' if socials_str else ''}\n{socials_str}\n\n"
                                f"🛍 <b>Приятных покупок!</b>",
                        "btn": "🛍 Перейти в магазин"
                    },
                    "uz": {
                        "text": f"🎉 <b>{shop.name}ga xush kelibsiz!</b>\n\n"
                                f"Sizni do'konimizda ko'rib turganimizdan xursandmiz. Endi siz buyurtmalaringiz holati va maxsus takliflar haqida bildirishnomalar olasiz.\n\n"
                                f"{'<b>Kontaktlar:</b>' if contacts_str else ''}\n{contacts_str}\n\n"
                                f"{'<b>Biz ijtimoiy tarmoqlarda:</b>' if socials_str else ''}\n{socials_str}\n\n"
                                f"🛍 <b>Xaridingiz barakali bo'lsin!</b>",
                        "btn": "🛍 Do'konni ochish"
                    },
                    "en": {
                        "text": f"🎉 <b>Welcome to {shop.name}!</b>\n\n"
                                f"We're glad to see you in our store. Now you will receive notifications about your orders status and special offers.\n\n"
                                f"{'<b>Contacts:</b>' if contacts_str else ''}\n{contacts_str}\n\n"
                                f"{'<b>Social Media:</b>' if socials_str else ''}\n{socials_str}\n\n"
                                f"🛍 <b>Happy shopping!</b>",
                        "btn": "🛍 Open Store"
                    }
                }
                
                t = welcome_data.get(lang, welcome_data["ru"])
                keyboard = {
                    "inline_keyboard": [[{"text": t["btn"], "url": shop_url}]]
                }
                
                # Send welcome with logo if available
                if shop.logo_url:
                    from app.core.config import settings
                    logo_abs_url = shop.logo_url
                    if not logo_abs_url.startswith('http'):
                        logo_abs_url = f"{settings.BASE_URL.rstrip('/')}/{logo_abs_url.lstrip('/')}"
                    
                    await send_telegram_photo(
                        shop.telegram_bot_token,
                        chat_id,
                        logo_abs_url,
                        caption=t["text"],
                        reply_markup=keyboard
                    )
                else:
                    await send_telegram_message(
                        shop.telegram_bot_token,
                        chat_id,
                        t["text"],
                        reply_markup=keyboard
                    )
                
    except Exception as e:
        logger.error(f"Error handling callback query: {e}", exc_info=True)


async def send_telegram_message(bot_token: str, chat_id: int, text: str, reply_markup: dict = None):
    """Send a message via Telegram Bot API"""
    import httpx
    from app.core.crypto import crypto
    
    try:
        token = bot_token
        if bot_token and ":" not in bot_token:
            decrypted = crypto.decrypt(bot_token)
            if decrypted: token = decrypted
        
        url = f"https://api.telegram.org/bot{token}/sendMessage"
        payload = {
            "chat_id": chat_id,
            "text": text,
            "parse_mode": "HTML",
            "disable_web_page_preview": False
        }
        if reply_markup:
            payload["reply_markup"] = reply_markup
        
        async with httpx.AsyncClient() as client:
            response = await client.post(url, json=payload)
            if response.status_code != 200:
                logger.error(f"Failed to send message: {response.text}")
    except Exception as e:
        logger.error(f"Error sending telegram message: {e}")

async def send_telegram_photo(bot_token: str, chat_id: int, photo_url: str, caption: str = "", reply_markup: dict = None):
    """Send a photo via Telegram Bot API"""
    import httpx
    from app.core.crypto import crypto
    
    try:
        token = bot_token
        if bot_token and ":" not in bot_token:
            decrypted = crypto.decrypt(bot_token)
            if decrypted: token = decrypted
            
        url = f"https://api.telegram.org/bot{token}/sendPhoto"
        payload = {
            "chat_id": chat_id,
            "photo": photo_url,
            "caption": caption,
            "parse_mode": "HTML"
        }
        if reply_markup:
            payload["reply_markup"] = reply_markup
            
        async with httpx.AsyncClient() as client:
            response = await client.post(url, json=payload)
            if response.status_code != 200:
                logger.error(f"Failed to send photo: {response.text}")
    except Exception as e:
        logger.error(f"Error sending telegram photo: {e}")

async def edit_telegram_message(bot_token: str, chat_id: int, message_id: int, text: str):
    """Edit an existing message via Telegram Bot API"""
    import httpx
    from app.core.crypto import crypto
    
    try:
        token = bot_token
        if bot_token and ":" not in bot_token:
            decrypted = crypto.decrypt(bot_token)
            if decrypted: token = decrypted
            
        url = f"https://api.telegram.org/bot{token}/editMessageText"
        payload = {
            "chat_id": chat_id,
            "message_id": message_id,
            "text": text,
            "parse_mode": "HTML"
        }
        
        async with httpx.AsyncClient() as client:
            await client.post(url, json=payload)
    except Exception as e:
        logger.error(f"Error editing telegram message: {e}")

async def delete_telegram_message(bot_token: str, chat_id: int, message_id: int):
    """Delete a message via Telegram Bot API"""
    import httpx
    from app.core.crypto import crypto
    
    try:
        token = bot_token
        if bot_token and ":" not in bot_token:
            decrypted = crypto.decrypt(bot_token)
            if decrypted: token = decrypted
            
        url = f"https://api.telegram.org/bot{token}/deleteMessage"
        payload = {
            "chat_id": chat_id,
            "message_id": message_id
        }
        
        async with httpx.AsyncClient() as client:
            await client.post(url, json=payload)
    except Exception as e:
        logger.error(f"Error deleting telegram message: {e}")

async def answer_callback_query(bot_token: str, callback_query_id: str, text: str = ""):
    """Answer a callback query"""
    import httpx
    from app.core.crypto import crypto
    
    try:
        token = bot_token
        if bot_token and ":" not in bot_token:
            decrypted = crypto.decrypt(bot_token)
            if decrypted: token = decrypted
            
        url = f"https://api.telegram.org/bot{token}/answerCallbackQuery"
        payload = {
            "callback_query_id": callback_query_id,
            "text": text
        }
        
        async with httpx.AsyncClient() as client:
            await client.post(url, json=payload)
    except Exception as e:
        logger.error(f"Error answering callback query: {e}")
