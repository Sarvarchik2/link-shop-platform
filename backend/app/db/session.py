from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.core.config import settings

engine_args = {}
if settings.SQLALCHEMY_DATABASE_URI.startswith("sqlite"):
    engine_args["connect_args"] = {"check_same_thread": False}

engine = create_engine(settings.SQLALCHEMY_DATABASE_URI, **engine_args)
print(f"Database engine created for: {settings.SQLALCHEMY_DATABASE_URI}")
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
