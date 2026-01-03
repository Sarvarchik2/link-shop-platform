from app.db.session import engine
from app.features.users.models import User
from app.core.security import verify_password
from sqlalchemy.orm import Session
from sqlalchemy import text

def check_user(phone, password):
    print(f"Checking user: {phone}")
    with Session(engine) as session:
        # Check DB connection
        try:
            res = session.execute(text("SELECT current_database();")).scalar()
            print(f"Connected to database: {res}")
        except Exception as e:
            print(f"DB Connection failed: {e}")
            return

        user = session.query(User).filter(User.phone == phone).first()
        if not user:
            print(f"❌ User with phone '{phone}' NOT FOUND in DB.")
            # List all users
            all_users = session.query(User).all()
            print(f"Found {len(all_users)} users in total:")
            for u in all_users:
                print(f" - {u.phone} (Role: {u.role})")
        else:
            print(f"✅ User found: ID={user.id}, Role={user.role}")
            if verify_password(password, user.password_hash):
                print("✅ Password verified successfully.")
            else:
                print("❌ Password verification FAILED.")

if __name__ == "__main__":
    check_user("998901234567", "owner123")
    print("-" * 20)
    check_user("998900000000", "admin123")
