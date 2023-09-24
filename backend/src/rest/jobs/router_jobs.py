from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from src.rest.repository import repo_job
from src import deps

router = APIRouter(prefix="/jobs")

@router.get("/all")
def get_all(db: Session = Depends(deps.get_db)):
    return repo_job.get_all(db)