from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from src import deps
from src.rest.repository import repo_tag

router = APIRouter(prefix='/tags')

@router.get('/all')
def read_all(db: Session = Depends(deps.get_db)):
    return repo_tag.get_all(db)

