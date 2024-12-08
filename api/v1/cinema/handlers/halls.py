from fastapi import Depends
from fastapi.requests import Request
from fastapi.routing import APIRouter

from api.v1.cinema.schemas import CreateHallCompleteSchema, CreateHallSchema
from apps.cinema.use_cases.hall_create import CreateHallUseCase
from core.containers import get_container
from core.schemas.responses.api_response import ApiResponse

router = APIRouter()


@router.post("")
async def create_hall_handler(
    request: Request,
    hall_data: CreateHallSchema,
    container=Depends(get_container),  # noqa: B008
) -> ApiResponse[CreateHallCompleteSchema]:
    use_case: CreateHallUseCase = container.resolve(CreateHallUseCase)
    hall_data = hall_data.model_dump()
    hall = await use_case.execute(hall_data=hall_data)
    return ApiResponse(
        data=CreateHallCompleteSchema(id=hall.id, title=hall.title)
    )
