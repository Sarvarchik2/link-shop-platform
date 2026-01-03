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
            print("Adding delivery_settings column...")
            connection.execute(text("ALTER TABLE shop ADD COLUMN IF NOT EXISTS delivery_settings JSON DEFAULT '{}'"))
            connection.commit()
            print("Successfully added delivery_settings column")
        except Exception as e:
            print(f"Error: {e}")
            # Try rolling back if needed, though DDL often auto-commits or can't be rolled back easily in some modes
            # But here we are in a transaction block
            pass

if __name__ == "__main__":
    migrate()
