import sys
import os

# Ensure the current directory is in the python path
sys.path.append(os.getcwd())

from app.db.session import SessionLocal
from app.features.users.models import User
from app.features.users.security import get_password_hash

def create_admin(phone, password, first_name="Admin", last_name="User"):
    db = SessionLocal()
    try:
        user = db.query(User).filter(User.phone == phone).first()
        if user:
            print(f"User with phone {phone} already exists. promoting to platform_admin...")
            user.role = "platform_admin"
            # reset password if provided (optional, good for recovery)
            # user.hashed_password = get_password_hash(password) 
        else:
            print(f"Creating new platform_admin user: {phone}")
            user = User(
                phone=phone,
                hashed_password=get_password_hash(password),
                first_name=first_name,
                last_name=last_name,
                role="platform_admin",
                is_active=True
            )
            db.add(user)
        
        db.commit()
        print("Success! User is now a platform_admin.")
        
    except Exception as e:
        print(f"Error: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python create_admin.py <phone> <password> [first_name] [last_name]")
        print("Example: python create_admin.py +998901234567 mysecretpassword")
        sys.exit(1)
        
    phone = sys.argv[1]
    password = sys.argv[2]
    first_name = sys.argv[3] if len(sys.argv) > 3 else "Platform"
    last_name = sys.argv[4] if len(sys.argv) > 4 else "Admin"
    
    create_admin(phone, password, first_name, last_name)
