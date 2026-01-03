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
            print("Adding delivery_cost column to order table...")
            # Note: 'order' is a reserved keyword in SQL, usually SQLAlchemy quotes it. 
            # In Postgres it's 'order' or "order". SQLAlchemy Table name is 'order' in models.py?
            # Let's check init_test_data.py or models.py for __tablename__. 
            # Base class usually defaults to lowercase class name. So 'order'.
            # Postgres requires quotes for "order".
            connection.execute(text('ALTER TABLE "order" ADD COLUMN IF NOT EXISTS delivery_cost FLOAT DEFAULT 0.0'))
            connection.commit()
            print("Successfully added delivery_cost column")
        except Exception as e:
            print(f"Error: {e}")
            pass

if __name__ == "__main__":
    migrate()
