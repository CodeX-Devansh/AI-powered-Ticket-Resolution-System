from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
import os
from dotenv import load_dotenv

load_dotenv()

db_url = os.getenv("DATABASE_URL")

if not db_url:
    raise RuntimeError("DATABASE_URL is not set")

if db_url.startswith("sqlite"):
    engine = create_engine(
        db_url,
        connect_args={"check_same_thread": False}
    )
else:
    engine = create_engine(db_url)

session = sessionmaker(bind=engine)

Base = declarative_base()


def get_db():
    db = session()
    try:
        yield db
    finally:
        db.close()