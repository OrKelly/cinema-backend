from fastapi.routing import APIRouter

from api.v1.cinema.handlers import router as cinema_router
from api.v1.common.handlers import router as common_router
from api.v1.users.handlers import router as user_router

router = APIRouter(
    prefix="/v1",
)

router.include_router(router=cinema_router, prefix="/cinema", tags=["cinema"])
router.include_router(router=common_router, prefix="/common", tags=["common"])
router.include_router(router=user_router, prefix="/users", tags=["users"])
router.include_router(router=cinema_router, prefix="/cinema", tags=["cinema"])
