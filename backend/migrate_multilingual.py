"""
Migration script to add multilingual support to Product and Category models.

This script:
1. Adds new multilingual columns (name_uz, name_ru, name_en, etc.)
2. Migrates existing data to the new columns
3. Drops old single-language columns

Usage:
    python migrate_multilingual.py
"""

from sqlalchemy import create_engine, Column, String, text
from sqlalchemy.orm import sessionmaker
import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app.db.session import engine, SessionLocal

def migrate_multilingual():
    db = SessionLocal()
    
    try:
        print("Starting multilingual migration...")
        
        # ===========================================
        # STEP 1: Add new columns to Product table
        # ===========================================
        print("\n1. Adding new multilingual columns to Product table...")
        
        product_columns = [
            ("name_uz", "VARCHAR"),
            ("name_ru", "VARCHAR"),
            ("name_en", "VARCHAR"),
            ("description_uz", "VARCHAR"),
            ("description_ru", "VARCHAR"),
            ("description_en", "VARCHAR"),
            ("category_uz", "VARCHAR"),
            ("category_ru", "VARCHAR"),
            ("category_en", "VARCHAR"),
            ("brand_uz", "VARCHAR"),
            ("brand_ru", "VARCHAR"),
            ("brand_en", "VARCHAR"),
        ]
        
        for col_name, col_type in product_columns:
            try:
                db.execute(text(f"ALTER TABLE product ADD COLUMN {col_name} {col_type}"))
                print(f"  ✓ Added column: {col_name}")
            except Exception as e:
                if "duplicate column name" in str(e).lower() or "already exists" in str(e).lower():
                    print(f"  ⚠ Column {col_name} already exists, skipping...")
                else:
                    raise
        
        db.commit()
        
        # ===========================================
        # STEP 2: Migrate existing Product data
        # ===========================================
        print("\n2. Migrating existing Product data...")
        
        db.execute(text("""
            UPDATE product 
            SET 
                name_uz = name,
                name_ru = name,
                name_en = name,
                description_uz = description,
                description_ru = description,
                description_en = description,
                category_uz = category,
                category_ru = category,
                category_en = category,
                brand_uz = brand,
                brand_ru = brand,
                brand_en = brand
            WHERE name_uz IS NULL
        """))
        
        db.commit()
        print("  ✓ Migrated Product data to multilingual fields")
        
        # ===========================================
        # STEP 3: Add new columns to Category table
        # ===========================================
        print("\n3. Adding new multilingual columns to Category table...")
        
        category_columns = [
            ("name_uz", "VARCHAR"),
            ("name_ru", "VARCHAR"),
            ("name_en", "VARCHAR"),
        ]
        
        for col_name, col_type in category_columns:
            try:
                db.execute(text(f"ALTER TABLE category ADD COLUMN {col_name} {col_type}"))
                print(f"  ✓ Added column: {col_name}")
            except Exception as e:
                if "duplicate column name" in str(e).lower() or "already exists" in str(e).lower():
                    print(f"  ⚠ Column {col_name} already exists, skipping...")
                else:
                    raise
        
        db.commit()
        
        # ===========================================
        # STEP 4: Migrate existing Category data
        # ===========================================
        print("\n4. Migrating existing Category data...")
        
        db.execute(text("""
            UPDATE category 
            SET 
                name_uz = name,
                name_ru = name,
                name_en = name
            WHERE name_uz IS NULL
        """))
        
        db.commit()
        print("  ✓ Migrated Category data to multilingual fields")
        
        # ===========================================
        # STEP 5: Drop old columns (commented out for safety)
        # ===========================================
        print("\n5. Old columns retained for backup (uncomment code to drop)")
        # Uncomment these lines after verifying migration worked correctly:
        
        # print("  Dropping old Product columns...")
        # db.execute(text("ALTER TABLE product DROP COLUMN name"))
        # db.execute(text("ALTER TABLE product DROP COLUMN description"))
        # db.execute(text("ALTER TABLE product DROP COLUMN category"))
        # db.execute(text("ALTER TABLE product DROP COLUMN brand"))
        # db.commit()
        
        # print("  Dropping old Category columns...")
        # db.execute(text("ALTER TABLE category DROP COLUMN name"))
        # db.commit()
        
        print("\n✅ Migration completed successfully!")
        print("\nNext steps:")
        print("1. Verify the data in your database")
        print("2. Update frontend to display multilingual fields")
        print("3. Uncomment DROP COLUMN statements in this script and run again to clean up")
        
    except Exception as e:
        print(f"\n❌ Migration failed: {e}")
        db.rollback()
        raise
    finally:
        db.close()

if __name__ == "__main__":
    migrate_multilingual()
