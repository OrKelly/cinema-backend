from fastapi import Depends
from fastapi.routing import APIRouter
from fastapi.requests import Request

from api.v1.cinema.schemas import CreateHallSchema, CreateHallCompleteSchema
from core.containers import get_container
from core.schemas.responses.api_response import ApiResponse
from apps.cinema.use_cases.hall_create import CreateHallUseCase

router = APIRouter()


@router.post('')
async def create_hall_handler(
        request: Request,
        hall_data: CreateHallSchema,
        container=Depends(get_container),  # noqa: B008
) -> ApiResponse[CreateHallCompleteSchema]:
    use_case: CreateHallUseCase = container.resolve(CreateHallUseCase)
    hall_data = hall_data.model_dump()
    hall = await use_case.execute(hall_data=hall_data)
    return ApiResponse(data=CreateHallCompleteSchema(id=hall.id, title=hall.title))
