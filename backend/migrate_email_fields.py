from sqlalchemy import text
from app.db.session import engine
from app.core.config import settings

def migrate():
    print("Adding email fields to user table...")
    fields = [
        ('ALTER TABLE "user" ADD COLUMN email VARCHAR;', 'email'),
        ('CREATE UNIQUE INDEX ix_user_email ON "user" (email);', 'email index'),
        ('ALTER TABLE "user" ADD COLUMN is_email_verified BOOLEAN DEFAULT FALSE;', 'is_email_verified'),
        ('ALTER TABLE "user" ADD COLUMN email_verification_code VARCHAR;', 'email_verification_code'),
        ('ALTER TABLE "user" ADD COLUMN verification_expires_at TIMESTAMP;', 'verification_expires_at'),
        ('ALTER TABLE "user" ADD COLUMN reset_password_token VARCHAR;', 'reset_password_token'),
        ('ALTER TABLE "user" ADD COLUMN reset_password_expires_at TIMESTAMP;', 'reset_password_expires_at')
    ]
    
    for sql, name in fields:
        with engine.begin() as conn:
            try:
                conn.execute(text(sql))
                print(f"Successfully added/created: {name}")
            except Exception as e:
                print(f"Skipping {name}: it may already exist. Error: {e}")

    print("Migration finished!")

if __name__ == "__main__":
    migrate()
