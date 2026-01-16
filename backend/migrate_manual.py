import sqlite3
import os

def migrate():
    db_path = "database.db"
    if not os.path.exists(db_path):
        print("Database not found")
        return
    
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    try:
        # Check shop table
        cursor.execute("PRAGMA table_info(shop)")
        columns = [row[1] for row in cursor.fetchall()]
        
        if "telegram_bot_token" not in columns:
            print("Adding telegram_bot_token to shop...")
            cursor.execute("ALTER TABLE shop ADD COLUMN telegram_bot_token VARCHAR")
        
        if "is_bot_active" not in columns:
            print("Adding is_bot_active to shop...")
            cursor.execute("ALTER TABLE shop ADD COLUMN is_bot_active BOOLEAN DEFAULT 0")

        # Re-check subscriptionplan (just in case)
        cursor.execute("PRAGMA table_info(subscriptionplan)")
        columns = [row[1] for row in cursor.fetchall()]
        if "can_broadcast" not in columns:
            print("Adding can_broadcast to subscriptionplan...")
            cursor.execute("ALTER TABLE subscriptionplan ADD COLUMN can_broadcast BOOLEAN DEFAULT 0")
        
        conn.commit()
        print("Migration completed successfully!")
    except Exception as e:
        print(f"Migration error: {e}")
    finally:
        conn.close()

if __name__ == "__main__":
    migrate()
