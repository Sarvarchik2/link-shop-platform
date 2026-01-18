import httpx
import os
from datetime import datetime
from app.core.celery_app import celery_app
from app.db.session import SessionLocal
from .models import Broadcast, BroadcastStatus
from app.features.shops.models import Shop, UserStoreTelegram
import logging
import time

logger = logging.getLogger(__name__)

@celery_app.task(name="app.features.broadcasts.tasks.send_broadcast_task")
def send_broadcast_task(broadcast_id: int):
    db = SessionLocal()
    broadcast = None
    try:
        logger.info(f"🚀 Starting broadcast task for broadcast_id={broadcast_id}")
        
        broadcast = db.query(Broadcast).filter(Broadcast.id == broadcast_id).first()
        if not broadcast:
            logger.warning(f"⚠️ Broadcast {broadcast_id} not found")
            return
        
        if broadcast.status != BroadcastStatus.PENDING:
            logger.warning(f"⚠️ Broadcast {broadcast_id} has status {broadcast.status}, expected PENDING")
            return

        shop = db.query(Shop).filter(Shop.id == broadcast.shop_id).first()
        if not shop:
            logger.error(f"❌ Shop {broadcast.shop_id} not found for broadcast {broadcast_id}")
            broadcast.status = BroadcastStatus.FAILED
            db.commit()
            return
            
        if not shop.telegram_bot_token:
            logger.error(f"❌ Shop {shop.id} has no telegram_bot_token")
            broadcast.status = BroadcastStatus.FAILED
            db.commit()
            return

        # Decrypt token
        from app.core.crypto import crypto
        token = crypto.decrypt(shop.telegram_bot_token)
        if not token:
            logger.error(f"❌ Failed to decrypt bot token for shop {shop.id}")
            broadcast.status = BroadcastStatus.FAILED
            db.commit()
            return

        logger.info(f"✓ Bot token decrypted for shop {shop.id}")
        broadcast.status = BroadcastStatus.SENDING
        db.commit()

        # Get audience
        if broadcast.audience_type == "recent":
            logger.info(f"📊 Getting recipients with audience_type='recent'")
            from app.features.orders.models import Order
            from datetime import timedelta
            thirty_days_ago = datetime.utcnow() - timedelta(days=30)
            
            # Optimized join query: get recipients who made an order in last 30 days
            query = db.query(UserStoreTelegram).join(
                Order, Order.user_id == UserStoreTelegram.user_id
            ).filter(
                UserStoreTelegram.store_id == shop.id,
                Order.shop_id == shop.id,
                Order.created_at >= thirty_days_ago
            ).distinct()
        else:
            logger.info(f"📊 Getting recipients with audience_type='{broadcast.audience_type}'")
            query = db.query(UserStoreTelegram).filter(UserStoreTelegram.store_id == shop.id)
        
        recipients = query.all()
        broadcast.total_count = len(recipients)
        db.commit()
        
        logger.info(f"👥 Found {len(recipients)} recipients for broadcast {broadcast_id}")
        
        if len(recipients) == 0:
            logger.warning(f"⚠️ No recipients found for broadcast {broadcast_id}. Check UserStoreTelegram table.")
            broadcast.status = BroadcastStatus.COMPLETED
            broadcast.completed_at = datetime.utcnow()
            db.commit()
            return

        sent_count = 0
        failed_count = 0

        with httpx.Client() as client:
            for idx, recipient in enumerate(recipients, 1):
                logger.debug(f"📤 Sending message {idx}/{len(recipients)} to chat_id={recipient.telegram_chat_id}")
                
                # Validate button_url - must be a valid HTTP/HTTPS URL
                button_url_to_send = None
                if broadcast.button_url:
                    url_lower = broadcast.button_url.lower().strip()
                    if url_lower.startswith('http://') or url_lower.startswith('https://'):
                        button_url_to_send = broadcast.button_url
                    else:
                        logger.warning(f"⚠️ Invalid button_url '{broadcast.button_url}' - skipping button for broadcast {broadcast.id}")
                
                success, error_msg = send_telegram_message_callback(
                    client,
                    token, 
                    recipient.telegram_chat_id, 
                    broadcast.message_text,
                    broadcast.media_url,
                    broadcast.button_text,
                    button_url_to_send
                )
                if success:
                    sent_count += 1
                else:
                    failed_count += 1
                    logger.warning(f"⚠️ Failed to send to chat_id={recipient.telegram_chat_id}: {error_msg}")
                
                # Update counts every 10 messages
                if (sent_count + failed_count) % 10 == 0:
                    broadcast.sent_count = sent_count
                    broadcast.failed_count = failed_count
                    db.commit()
                    logger.info(f"📊 Progress: {sent_count} sent, {failed_count} failed out of {len(recipients)}")

                # Limit: 30 messages per second -> 0.05s delay is safe
                time.sleep(0.05)

        broadcast.sent_count = sent_count
        broadcast.failed_count = failed_count
        broadcast.status = BroadcastStatus.COMPLETED
        broadcast.completed_at = datetime.utcnow()
        db.commit()
        
        logger.info(f"✅ Broadcast {broadcast_id} completed: {sent_count} sent, {failed_count} failed")

    except Exception as e:
        logger.error(f"❌ Error in send_broadcast_task for broadcast {broadcast_id}: {e}", exc_info=True)
        if broadcast:
            broadcast.status = BroadcastStatus.FAILED
            db.commit()
    finally:
        db.close()

def send_telegram_message_callback(client, token, chat_id, text, media_url=None, button_text=None, button_url=None):
    """
    Returns: tuple (success: bool, error_message: str)
    """
    try:
        reply_markup = None
        if button_text and button_url:
            reply_markup = {
                "inline_keyboard": [[{"text": button_text, "url": button_url}]]
            }

        if media_url:
            is_video = any(media_url.lower().endswith(ext) for ext in ['.mp4', '.mov', '.avi'])
            method = "sendVideo" if is_video else "sendPhoto"
            payload = {
                "chat_id": chat_id,
                method.replace("send", "").lower(): media_url,
                "caption": text,
            }
            if reply_markup:
                payload["reply_markup"] = reply_markup
            
            url = f"https://api.telegram.org/bot{token}/{method}"
        else:
            url = f"https://api.telegram.org/bot{token}/sendMessage"
            payload = {
                "chat_id": chat_id,
                "text": text,
            }
            if reply_markup:
                payload["reply_markup"] = reply_markup

        resp = client.post(url, json=payload, timeout=10)
        
        if resp.status_code == 200:
            return (True, None)
        else:
            error_detail = f"HTTP {resp.status_code}: {resp.text[:200]}"
            logger.error(f"Telegram API error for chat_id {chat_id}: {error_detail}")
            return (False, error_detail)
            
    except Exception as e:
        error_msg = f"Exception: {str(e)}"
        logger.error(f"Telegram sync send error for chat_id {chat_id}: {error_msg}")
        return (False, error_msg)

