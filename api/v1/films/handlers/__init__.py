from fastapi import APIRouter

from .films import router as films_router
from .sessions import router as session_router

router = APIRouter()

router.include_router(router=films_router)
router.include_router(router=session_router, prefix="/sessions")
