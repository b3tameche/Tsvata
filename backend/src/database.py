from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from config import Config

engine = create_engine(Config.DB_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)