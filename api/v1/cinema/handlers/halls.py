from typing import Annotated

from fastapi import Depends, Path
from fastapi.requests import Request
from fastapi.routing import APIRouter

from api.v1.cinema.schemas import CreateHallCompleteSchema, CreateHallSchema
from api.v1.cinema.schemas.halls import GetHallSchema
from apps.cinema.services.halls import BaseHallService
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


@router.get("/{id}")
async def get_hall_handler(
    request: Request,
    id: Annotated[int, Path(gt=0, description="Enter hall id")],
    container=Depends(get_container),  # noqa: B008
) -> ApiResponse[GetHallSchema]:
    hall_service: BaseHallService = container.resolve(BaseHallService)
    hall = await hall_service.get_with_rows_and_places_by_id(id)
    return ApiResponse(data=GetHallSchema.to_schema(hall))
