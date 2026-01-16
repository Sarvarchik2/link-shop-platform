-- Migration: Add broadcast features to the platform
-- Date: 2026-01-17
-- Description: Adds can_broadcast column to subscriptionplan and telegram bot columns to shop

-- Add can_broadcast column to subscriptionplan
ALTER TABLE subscriptionplan ADD COLUMN IF NOT EXISTS can_broadcast BOOLEAN DEFAULT FALSE;

-- Add telegram bot integration columns to shop
ALTER TABLE shop ADD COLUMN IF NOT EXISTS telegram_bot_token VARCHAR;
ALTER TABLE shop ADD COLUMN IF NOT EXISTS is_bot_active BOOLEAN DEFAULT FALSE;

-- Update existing plans
UPDATE subscriptionplan SET can_broadcast = FALSE WHERE slug = 'trial';
UPDATE subscriptionplan SET can_broadcast = TRUE WHERE slug IN ('business', 'basic', 'premium');

-- If basic plan exists and business doesn't, rename it
UPDATE subscriptionplan 
SET slug = 'business', 
    name = 'Бизнес',
    description = 'Идеально для растущих магазинов с рассылками',
    features = 'До 200 товаров,Рассылки в Telegram (до 500/мес),Приоритетная поддержка'
WHERE slug = 'basic' AND NOT EXISTS (SELECT 1 FROM subscriptionplan WHERE slug = 'business');

-- Update premium plan description
UPDATE subscriptionplan 
SET description = 'Безлимитные возможности для вашего бренда',
    features = 'Безлимитные товары,Безлимитные рассылки,Подробная статистика,Личный менеджер'
WHERE slug = 'premium';

-- Create broadcast table if not exists
CREATE TABLE IF NOT EXISTS broadcast (
    id SERIAL PRIMARY KEY,
    shop_id INTEGER NOT NULL REFERENCES shop(id) ON DELETE CASCADE,
    message_text TEXT NOT NULL,
    media_url VARCHAR,
    button_text VARCHAR,
    button_url VARCHAR,
    audience_type VARCHAR DEFAULT 'all',
    status VARCHAR DEFAULT 'draft',
    sent_count INTEGER DEFAULT 0,
    failed_count INTEGER DEFAULT 0,
    total_count INTEGER DEFAULT 0,
    scheduled_at TIMESTAMP,
    created_at TIMESTAMP DEFAULT NOW(),
    completed_at TIMESTAMP
);

-- Create index for broadcast queries
CREATE INDEX IF NOT EXISTS idx_broadcast_shop_id ON broadcast(shop_id);
CREATE INDEX IF NOT EXISTS idx_broadcast_status ON broadcast(status);
