from app.db.session import SessionLocal
from sqlalchemy import text

def fix_product_schema():
    db = SessionLocal()
    try:
        print("Fixing Product Schema...")
        
        try:
            print("Adding 'created_at' to product...")
            db.execute(text("ALTER TABLE product ADD COLUMN created_at TIMESTAMP DEFAULT NOW();"))
            print("Done.")
        except Exception as e:
            print(f"Skipping created_at: {e}")

        try:
            print("Adding 'updated_at' to product...")
            db.execute(text("ALTER TABLE product ADD COLUMN updated_at TIMESTAMP DEFAULT NOW();"))
            print("Done.")
        except Exception as e:
            print(f"Skipping updated_at: {e}")

        db.commit()
        print("Schema update committed.")
        
    except Exception as e:
        print(f"Global Error: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    fix_product_schema()
