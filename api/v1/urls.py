from fastapi.routing import APIRouter

from api.v1.cinema.handlers import router as cinema_router
from api.v1.common.handlers import router as common_router
from api.v1.employees.handlers import router as employee_router
from api.v1.films.handlers import router as film_router
from api.v1.orders.handlers import router as order_router
from api.v1.users.handlers import router as user_router

router = APIRouter(
    prefix="/v1",
)

router.include_router(router=cinema_router, prefix="/cinema", tags=["cinema"])
router.include_router(router=common_router, prefix="/common", tags=["common"])
router.include_router(
    router=employee_router, prefix="/employees", tags=["employees"]
)
router.include_router(router=film_router, prefix="/films", tags=["films"])
router.include_router(router=user_router, prefix="/users", tags=["users"])
router.include_router(router=order_router, prefix="/orders", tags=["orders"])
