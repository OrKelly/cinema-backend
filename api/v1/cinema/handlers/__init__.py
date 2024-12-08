from fastapi import APIRouter

from .halls import router as halls_router

router = APIRouter()

router.include_router(router=halls_router, prefix="/halls")
