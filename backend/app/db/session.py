from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.core.config import settings

engine_args = {
    "pool_pre_ping": True,  # Prevent "server closed connection" errors
}

if settings.SQLALCHEMY_DATABASE_URI.startswith("sqlite"):
    engine_args["connect_args"] = {"check_same_thread": False}
else:
    # Postgres specific optimizations
    engine_args.update({
        "pool_size": 20,
        "max_overflow": 10,
        "pool_timeout": 30,
        "pool_recycle": 1800,
    })

engine = create_engine(settings.SQLALCHEMY_DATABASE_URI, **engine_args)
print(f"Database engine created for: {settings.SQLALCHEMY_DATABASE_URI}")
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
