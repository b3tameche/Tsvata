from fastapi import APIRouter

from src.rest.company import router_company
from src.rest.jobs import router_jobs
from src.rest.tags import router_tags

router = APIRouter()

router.include_router(router_company.router, tags=["Company"])
router.include_router(router_jobs.router, tags=["Job"])
router.include_router(router_tags.router, tags=['Tag'])