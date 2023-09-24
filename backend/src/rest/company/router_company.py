from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from src import deps
from src.rest.repository import repo_company

router = APIRouter(prefix="/company")

@router.get("/all")
def read_all(db: Session = Depends(deps.get_db)):
    return repo_company.get_all(db)
