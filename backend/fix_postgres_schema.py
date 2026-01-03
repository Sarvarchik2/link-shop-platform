from app.db.session import SessionLocal
from sqlalchemy import text

def fix_postgres():
    db = SessionLocal()
    try:
        print("Fixing Postgres Schema...")
        
        # 1. Add 'type' to subscriptionrequest
        try:
            print("Adding 'type' to subscriptionrequest...")
            db.execute(text("ALTER TABLE subscriptionrequest ADD COLUMN type VARCHAR DEFAULT 'new';"))
            print("Done.")
        except Exception as e:
            print(f"Skipping subscriptionrequest type: {e}")

        # 2. Add multilingual columns to banner
        banner_cols = [
            'title_ru', 'title_en', 'title_uz',
            'subtitle_ru', 'subtitle_en', 'subtitle_uz',
            'button_text_ru', 'button_text_en', 'button_text_uz'
        ]
        
        for col in banner_cols:
            try:
                print(f"Adding '{col}' to banner...")
                db.execute(text(f"ALTER TABLE banner ADD COLUMN {col} VARCHAR;"))
                print("Done.")
            except Exception as e:
                 # Postgres raises error if column exists. We can ignore or catch specific code.
                 # "duplicate column name"
                print(f"Skipping {col}: {e}")

        db.commit()
        print("Schema update committed.")
        
    except Exception as e:
        print(f"Global Error: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    fix_postgres()
