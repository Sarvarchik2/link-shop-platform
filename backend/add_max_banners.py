import sys
import os

# Add the parent directory to sys.path
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.insert(0, parent_dir)
sys.path.insert(0, os.path.join(parent_dir, "app"))

from app.db.session import engine
from sqlalchemy import text

def migrate():
    with engine.connect() as connection:
        try:
            print("Adding max_banners column to subscriptionplan...")
            connection.execute(text("ALTER TABLE subscriptionplan ADD COLUMN IF NOT EXISTS max_banners INTEGER DEFAULT 1"))
            connection.commit()
            print("Successfully added max_banners column")
        except Exception as e:
            print(f"Error: {e}")
            pass

if __name__ == "__main__":
    migrate()
