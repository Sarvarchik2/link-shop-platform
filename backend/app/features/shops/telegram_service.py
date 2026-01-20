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
        
        # 2. Find user chat_id and language for this shop
        mapping = db.query(UserStoreTelegram).filter(
            UserStoreTelegram.user_id == user_id,
            UserStoreTelegram.store_id == shop_id
        ).first()
        
        if not mapping:
            logger.info(f"Chat ID not found for user {user_id} in shop {shop_id}")
            return
        
        lang = mapping.language or "ru"
        
        # Decrypt token
        from app.core.crypto import crypto
        token = crypto.decrypt(shop.telegram_bot_token)
        if not token:
            logger.error(f"Failed to decrypt bot token for shop {shop_id}")
            return
        
        # 4. Format message based on language
        translations = {
            "ru": {
                "title": f"📦 <b>Заказ №{order_id}</b> в магазине {shop_name}!",
                "status": "Статус изменен на:",
                "footer": "Спасибо, что выбрали нас!",
                "view_details": "📋 Подробнее в Web App",
                "statuses": {
                    "pending": "В ожидании ⏳",
                    "processing": "В процессе ⚙️",
                    "shipping": "В пути 🚚",
                    "delivered": "Доставлен ✅",
                    "cancelled": "Отменен ❌"
                }
            },
            "uz": {
                "title": f"📦 <b>{shop_name} do'konida {order_id}-sonli buyurtma!</b>",
                "status": "Holat o'zgardi:",
                "footer": "Bizni tanlaganingiz uchun rahmat!",
                "view_details": "📋 Web App-da batafsil",
                "statuses": {
                    "pending": "Kutilmoqda ⏳",
                    "processing": "Jarayonda ⚙️",
                    "shipping": "Yo'lda 🚚",
                    "delivered": "Yetkazildi ✅",
                    "cancelled": "Bekor qilindi ❌"
                }
            },
            "en": {
                "title": f"📦 <b>Order №{order_id}</b> in {shop_name}!",
                "status": "Status changed to:",
                "footer": "Thank you for choosing us!",
                "view_details": "📋 Details in Web App",
                "statuses": {
                    "pending": "Pending ⏳",
                    "processing": "Processing ⚙️",
                    "shipping": "Shipping 🚚",
                    "delivered": "Delivered ✅",
                    "cancelled": "Cancelled ❌"
                }
            }
        }
        
        t = translations.get(lang, translations["ru"])
        status_text = t["statuses"].get(new_status, new_status)
        
        message = f"{t['title']}\n\n{t['status']} <b>{status_text}</b>\n\n{t['footer']}"
        
        # Add button to open bot
        keyboard = {
            "inline_keyboard": [
                [{"text": t["view_details"], "url": f"https://t.me/{shop.slug}_bot"}] # Assuming bot username matches slug
            ]
        }
        # Fallback to general shop link if bot username is unknown or use the web app link
        shop_url = f"https://storely.uz/s/{shop.slug}"
        keyboard["inline_keyboard"][0][0]["url"] = shop_url

        # 5. Send message
        async with httpx.AsyncClient() as client:
            try:
                url = f"https://api.telegram.org/bot{token}/sendMessage"
                payload = {
                    "chat_id": mapping.telegram_chat_id,
                    "text": message,
                    "parse_mode": "HTML",
                    "reply_markup": keyboard
                }
                response = await client.post(url, json=payload)
                if response.status_code != 200:
                    logger.error(f"Telegram API error: {response.text}")
            except Exception as e:
                logger.error(f"Failed to send telegram notification: {str(e)}")

    async def send_new_order_notification(self, db: Session, shop_id: int, order_id: int, total_price: float, customer_name: str):
        """Notify shop owner about new order with full details"""
        from app.features.orders.models import Order, OrderItem
        from app.features.products.models import Product
        
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
        
        # Fetch full order details
        order = db.query(Order).filter(Order.id == order_id).first()
        items = db.query(OrderItem, Product.name_ru).join(Product).filter(OrderItem.order_id == order_id).all()
        
        # Build items list string
        items_str = ""
        for item, name in items:
            items_str += f"• {name} x{item.quantity} — {item.price * item.quantity} сум\n"
            if item.selected_color or item.selected_size:
                variants = []
                if item.selected_color: variants.append(item.selected_color)
                if item.selected_size: variants.append(item.selected_size)
                items_str += f"  ({', '.join(variants)})\n"
        
        lang = mapping.language or "ru"
        
        # Message for owner (keeping it mostly RU for now if owner is likely RU speaker, but can translate if needed)
        # Detailed message required by user
        message = (
            f"🆕 <b>Новый заказ №{order_id}!</b>\n\n"
            f"👤 <b>Покупатель:</b> {customer_name}\n"
            f"📞 <b>Контакт:</b> {order.delivery_phone}\n"
            f"📍 <b>Адрес:</b> {order.delivery_city}, {order.delivery_address}\n\n"
            f"📦 <b>Товары:</b>\n{items_str}\n"
            f"💰 <b>ИТОГО: {total_price} сум</b>\n\n"
            f"Управляйте заказами в панели управления."
        )
        
        keyboard = {
            "inline_keyboard": [
                [{"text": "⚙️ Управление заказом", "url": f"https://storely.uz/admin/orders"}]
            ]
        }
        
        async with httpx.AsyncClient() as client:
            try:
                url = f"https://api.telegram.org/bot{token}/sendMessage"
                await client.post(url, json={
                    "chat_id": mapping.telegram_chat_id,
                    "text": message,
                    "parse_mode": "HTML",
                    "reply_markup": keyboard
                })
            except Exception as e:
                logger.error(f"Error sending owner notification: {e}")

    async def send_order_confirmation(self, db: Session, order_id: int, shop_id: int, user_id: int, shop_name: str, total_price: float):
        """Notify customer that their order has been received"""
        shop = db.query(Shop).filter(Shop.id == shop_id).first()
        if not shop or not shop.is_bot_active or not shop.telegram_bot_token:
            return
            
        mapping = db.query(UserStoreTelegram).filter(
            UserStoreTelegram.user_id == user_id,
            UserStoreTelegram.store_id == shop_id
        ).first()
        
        if not mapping:
            return
            
        from app.core.crypto import crypto
        token = crypto.decrypt(shop.telegram_bot_token)
        if not token: return
        
        lang = mapping.language or "ru"
        
        translations = {
            "ru": {
                "text": f"✅ <b>Ваш заказ №{order_id} принят!</b>\n\nМагазин: {shop_name}\nСумма: {total_price} сум\n\nДля отслеживания статуса и просмотра деталей откройте наш Web App.",
                "button": "📋 Открыть Web App"
            },
            "uz": {
                "text": f"✅ <b>Sizning {order_id}-sonli buyurtmangiz qabul qilindi!</b>\n\nDo'kon: {shop_name}\nSumma: {total_price} so'm\n\nHolatni kuzatish va tafsilotlarni ko'rish uchun Web App-ni oching.",
                "button": "📋 Web App-ni ochish"
            },
            "en": {
                "text": f"✅ <b>Your order №{order_id} has been received!</b>\n\nShop: {shop_name}\nTotal: {total_price} sum\n\nTo track status and view details, open our Web App.",
                "button": "📋 Open Web App"
            }
        }
        
        t = translations.get(lang, translations["ru"])
        
        keyboard = {
            "inline_keyboard": [
                [{"text": t["button"], "url": f"https://storely.uz/s/{shop.slug}"}]
            ]
        }
        
        async with httpx.AsyncClient() as client:
            try:
                url = f"https://api.telegram.org/bot{token}/sendMessage"
                await client.post(url, json={
                    "chat_id": mapping.telegram_chat_id,
                    "text": t["text"],
                    "parse_mode": "HTML",
                    "reply_markup": keyboard
                })
            except Exception as e:
                logger.error(f"Error sending customer confirmation: {e}")

telegram_notification_service = TelegramNotificationService()
