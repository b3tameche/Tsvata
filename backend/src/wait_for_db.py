import logging

from tenacity import retry, stop_after_attempt, wait_fixed, before_log, after_log

from database import SessionLocal

from sqlalchemy.orm import Session
from sqlalchemy import text

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

max_attempts = 24
delay_between = 5 # seconds between each try

@retry(
    stop=stop_after_attempt(max_attempts),
    wait=wait_fixed(delay_between),
    before=before_log(logger, logging.INFO),
    after=after_log(logger, logging.INFO)
)
def wait_for_db() -> None:
    try:
        db: Session = SessionLocal()
        db.execute(text("SELECT 1;"))
    except Exception as e:
        logger.error(e)
        raise e

if __name__ == "__main__":
    logger.info("Waiting for database")
    wait_for_db()
    logger.info("Database successfully initialized")