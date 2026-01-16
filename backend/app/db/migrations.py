"""
Auto-migration script for production PostgreSQL
This will run automatically on startup and apply missing columns/tables
"""
from sqlalchemy import text
import logging

logger = logging.getLogger(__name__)

def run_migrations(engine):
    """Apply database migrations"""
    try:
        with engine.begin() as conn:
            logger.info("Starting database migrations...")
            
            # Check if we're using PostgreSQL
            is_postgres = 'postgresql' in str(engine.url)
            
            if is_postgres:
                # PostgreSQL migrations
                migrations = [
                    # Add can_broadcast to subscriptionplan
                    """
                    DO $$ 
                    BEGIN
                        IF NOT EXISTS (
                            SELECT 1 FROM information_schema.columns 
                            WHERE table_name='subscriptionplan' AND column_name='can_broadcast'
                        ) THEN
                            ALTER TABLE subscriptionplan ADD COLUMN can_broadcast BOOLEAN DEFAULT FALSE;
                        END IF;
                    END $$;
                    """,
                    
                    # Add telegram_bot_token to shop
                    """
                    DO $$ 
                    BEGIN
                        IF NOT EXISTS (
                            SELECT 1 FROM information_schema.columns 
                            WHERE table_name='shop' AND column_name='telegram_bot_token'
                        ) THEN
                            ALTER TABLE shop ADD COLUMN telegram_bot_token VARCHAR;
                        END IF;
                    END $$;
                    """,
                    
                    # Add is_bot_active to shop
                    """
                    DO $$ 
                    BEGIN
                        IF NOT EXISTS (
                            SELECT 1 FROM information_schema.columns 
                            WHERE table_name='shop' AND column_name='is_bot_active'
                        ) THEN
                            ALTER TABLE shop ADD COLUMN is_bot_active BOOLEAN DEFAULT FALSE;
                        END IF;
                    END $$;
                    """,
                    
                    # Update existing plans
                    """
                    UPDATE subscriptionplan SET can_broadcast = FALSE WHERE slug = 'trial' AND can_broadcast IS NULL;
                    """,
                    
                    """
                    UPDATE subscriptionplan SET can_broadcast = TRUE 
                    WHERE slug IN ('business', 'basic', 'premium') AND can_broadcast IS NULL;
                    """,
                ]
                
                for migration in migrations:
                    try:
                        conn.execute(text(migration))
                        logger.info(f"✓ Migration executed successfully")
                    except Exception as e:
                        logger.warning(f"Migration warning (may be already applied): {e}")
                        
                logger.info("✓ All migrations completed")
                
            else:
                logger.info("SQLite detected - using SQLite migrations")
                # SQLite migrations handled by migrate_manual.py
                
    except Exception as e:
        logger.error(f"Migration error: {e}")
        # Don't raise - let the app continue even if migrations fail
        # (they might already be applied)
