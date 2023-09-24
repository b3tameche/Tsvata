from typing import Generator

import logging

from src.database import SessionLocal
from sqlalchemy.orm import Session

logger = logging.getLogger(__name__)

def get_db() -> Generator:
    try:
        db: Session = SessionLocal()
        yield db
    except Exception as e:
        logger.error(e)
    finally:
        db.close()