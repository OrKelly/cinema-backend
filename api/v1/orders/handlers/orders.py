from fastapi import APIRouter, Depends
from fastapi.requests import Request

from api.v1.orders.schemas.orders import OrderAddSchema, OrderCompleteSchema
from apps.orders.use_cases.order_create import CreateOrderUseCase
from core.containers import get_container
from core.schemas.responses.api_response import ApiResponse

router = APIRouter()


@router.post("/")
async def create_order_handler(
    request: Request,
    order_data: OrderAddSchema,  # noqa: B008
    container=Depends(get_container),  # noqa: B008
) -> ApiResponse[OrderCompleteSchema]:
    use_case: CreateOrderUseCase = container.resolve(CreateOrderUseCase)
    order_data = order_data.model_dump()
    if request.user:
        order_data["user_id"] = request.user.id
    order_ids = await use_case.execute(attributes=order_data)
    return ApiResponse(data=OrderCompleteSchema(order_ids=order_ids))
