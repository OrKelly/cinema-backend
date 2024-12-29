from fastapi import APIRouter

from .films import router as films_router

router = APIRouter()

router.include_router(router=films_router, prefix="/film")
