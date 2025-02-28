from fastapi import APIRouter

from .film_sessions import router as session_router
from .films import router as films_router

router = APIRouter()

router.include_router(router=films_router)
router.include_router(router=session_router, prefix="/sessions")
