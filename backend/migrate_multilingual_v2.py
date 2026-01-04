
import os
import sys

# Ensure the current directory is in the python path
sys.path.append(os.getcwd())

from sqlalchemy import text
from app.db.session import engine

def migrate():
    with engine.connect() as connection:
        print("Migrating database - Adding multilingual fields...")
        
        # 1. Update SubscriptionPlan table
        print("Updating SubscriptionPlan table...")
        columns_to_add = [
            ("name_ru", "VARCHAR"),
            ("name_en", "VARCHAR"),
            ("name_uz", "VARCHAR"),
            ("description_ru", "VARCHAR"),
            ("description_en", "VARCHAR"),
            ("description_uz", "VARCHAR"),
            ("features_ru", "VARCHAR"),
            ("features_en", "VARCHAR"),
            ("features_uz", "VARCHAR"),
        ]
        
        for col_name, col_type in columns_to_add:
            try:
                connection.execute(text(f"ALTER TABLE subscriptionplan ADD COLUMN {col_name} {col_type}"))
                print(f"  + Added column {col_name}")
            except Exception as e:
                print(f"  ! Column {col_name} might already exist or error: {e}")
                
        # 2. Update Offer table
        print("Updating Offer table...")
        columns_to_add_offer = [
            ("title_ru", "VARCHAR"),
            ("title_en", "VARCHAR"),
            ("title_uz", "VARCHAR"),
            ("description_ru", "VARCHAR"),
            ("description_en", "VARCHAR"),
            ("description_uz", "VARCHAR"),
            ("price_text_ru", "VARCHAR"),
            ("price_text_en", "VARCHAR"),
            ("price_text_uz", "VARCHAR"),
            ("contact_text_ru", "VARCHAR"),
            ("contact_text_en", "VARCHAR"),
            ("contact_text_uz", "VARCHAR"),
        ]
        
        for col_name, col_type in columns_to_add_offer:
            try:
                connection.execute(text(f"ALTER TABLE offer ADD COLUMN {col_name} {col_type}"))
                print(f"  + Added column {col_name}")
            except Exception as e:
                print(f"  ! Column {col_name} might already exist or error: {e}")
                
        connection.commit()
        print("Migration complete!")

if __name__ == "__main__":
    migrate()
