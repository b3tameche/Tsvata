from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy import create_engine

from src.config import Config

class create_session:
    def __init__(self):
        engine = create_engine(Config.DB_URL)
        SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
        self.session: Session = SessionLocal()
    
    def __enter__(self):
        return self.session

    def __exit__(self, type, val, tb):
        self.session.close()