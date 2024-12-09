from fastapi import APIRouter

from .halls import router as halls_router
from .rows import router as rows_router

router = APIRouter()

router.include_router(router=halls_router, prefix="/halls")
router.include_router(router=rows_router, prefix="/rows")
