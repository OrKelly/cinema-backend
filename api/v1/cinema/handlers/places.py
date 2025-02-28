from fastapi import Depends
from fastapi.requests import Request
from fastapi.routing import APIRouter

from api.v1.cinema.schemas.places import (
    CreatePlaceCompleteSchema,
    CreatePlaceSchema,
)
from apps.cinema.use_cases.place_create import CreatePlaceUseCase
from core.containers import get_container
from core.schemas.responses.api_response import ApiResponse

router = APIRouter()


@router.post("")
async def create_place_handler(
    request: Request,
    place_schema: CreatePlaceSchema,
    container=Depends(get_container),  # noqa: B008
) -> ApiResponse[CreatePlaceCompleteSchema]:
    use_case: CreatePlaceUseCase = container.resolve(CreatePlaceUseCase)
    place_data = place_schema.model_dump()
    place = await use_case.execute(place_data)
    return ApiResponse(
        data=CreatePlaceCompleteSchema(
            id=place.id, row=place.row_id, number=place.number
        )
    )
