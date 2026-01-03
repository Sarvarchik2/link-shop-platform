from app.db.session import SessionLocal
from sqlalchemy import text

def add_column():
    db = SessionLocal()
    try:
        print("Adding 'type' column to subscriptionrequest...")
        db.execute(text("ALTER TABLE subscriptionrequest ADD COLUMN type VARCHAR DEFAULT 'new';"))
        db.commit()
        print("Column added successfully.")
    except Exception as e:
        print(f"Error: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    add_column()
