from fastapi.routing import APIRouter

from api.v1.common.handlers import router as common_router

router = APIRouter(
    prefix="/v1",
)

router.include_router(router=common_router, prefix="/common", tags=["common"])
