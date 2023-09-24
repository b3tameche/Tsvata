from sqlalchemy.orm import Session
from sqlalchemy import text, CursorResult, Row

def get_all(db: Session):

    sql = text("SELECT * FROM tags;")

    cr: CursorResult = db.execute(sql)

    rows = [row._mapping for row in cr.all()]

    return rows