from sqlalchemy.orm import Session
from sqlalchemy import text, CursorResult

def get_all(db: Session):
    """Retrieves all company entries from database"""

    sql = text("SELECT * FROM companies;")

    cr: CursorResult = db.execute(sql)

    rows = [row._mapping for row in cr.all()]

    return rows
