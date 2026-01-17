import httpx
import logging
from sqlalchemy.orm import Session
from app.features.shops.models import Shop, UserStoreTelegram

logger = logging.getLogger(__name__)

class TelegramNotificationService:
    async def send_order_status_update(self, db: Session, order_id: int, shop_id: int, user_id: int, new_status: str, shop_name: str):
        # 1. Check if shop has telegram bot active
        shop = db.query(Shop).filter(Shop.id == shop_id).first()
        if not shop or not shop.is_bot_active or not shop.telegram_bot_token:
            return
        
        # 2. Find user chat_id for this shop
        mapping = db.query(UserStoreTelegram).filter(
            UserStoreTelegram.user_id == user_id,
            UserStoreTelegram.store_id == shop_id
        ).first()
        
        if not mapping:
            logger.info(f"Chat ID not found for user {user_id} in shop {shop_id}")
            return
        
        # Decrypt token
        from app.core.crypto import crypto
        token = crypto.decrypt(shop.telegram_bot_token)
        if not token:
            logger.error(f"Failed to decrypt bot token for shop {shop_id}")
            return
        
        # 4. Format message
        status_map = {
            "pending": "В ожидании ⏳",
            "processing": "В процессе ⚙️",
            "shipping": "В пути 🚚",
            "delivered": "Доставлен ✅",
            "cancelled": "Отменен ❌"
        }
        status_text = status_map.get(new_status, new_status)
        
        message = f"📦 <b>Заказ №{order_id}</b> в магазине {shop_name}!\n\nСтатус изменен на: <b>{status_text}</b>\n\nСпасибо, что выбрали нас!"
        
        # 5. Send message
        async with httpx.AsyncClient() as client:
            try:
                url = f"https://api.telegram.org/bot{token}/sendMessage"
                payload = {
                    "chat_id": mapping.telegram_chat_id,
                    "text": message,
                    "parse_mode": "HTML"
                }
                response = await client.post(url, json=payload)
                if response.status_code != 200:
                    logger.error(f"Telegram API error: {response.text}")
            except Exception as e:
                logger.error(f"Failed to send telegram notification: {str(e)}")

    async def send_new_order_notification(self, db: Session, shop_id: int, order_id: int, total_price: float, customer_name: str):
        """Notify shop owner about new order"""
        shop = db.query(Shop).filter(Shop.id == shop_id).first()
        if not shop or not shop.is_bot_active or not shop.telegram_bot_token:
            return
            
        # Find OWNER chat_id
        mapping = db.query(UserStoreTelegram).filter(
            UserStoreTelegram.user_id == shop.owner_id,
            UserStoreTelegram.store_id == shop.id
        ).first()
        
        if not mapping:
            return
            
        from app.core.crypto import crypto
        token = crypto.decrypt(shop.telegram_bot_token)
        if not token: return
        
        message = (
            f"🆕 <b>Новый заказ №{order_id}!</b>\n\n"
            f"👤 Покупатель: {customer_name}\n"
            f"💰 Сумма: {total_price} сум\n\n"
            f"Управляйте заказами в панели управления."
        )
        
        async with httpx.AsyncClient() as client:
            try:
                url = f"https://api.telegram.org/bot{token}/sendMessage"
                await client.post(url, json={
                    "chat_id": mapping.telegram_chat_id,
                    "text": message,
                    "parse_mode": "HTML"
                })
            except Exception as e:
                logger.error(f"Error sending owner notification: {e}")

telegram_notification_service = TelegramNotificationService()
