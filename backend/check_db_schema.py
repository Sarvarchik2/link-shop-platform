from app.db.session import SessionLocal
from sqlalchemy import text, inspect

def check_db():
    db = SessionLocal()
    try:
        inspector = inspect(db.get_bind())
        tables = inspector.get_table_names()
        print("Tables in DB:")
        for table in tables:
            print(f"- {table}")
            
        targets = ['subscriptionrequest', 'subscription_request', 'banner']
        for table in targets:
             if table in tables:
                print(f"\nColumns in {table}:")
                columns = inspector.get_columns(table)
                for col in columns:
                    print(f"- {col['name']}: {col['type']}")
             else:
                pass 

    except Exception as e:
        print(f"Error: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    check_db()
