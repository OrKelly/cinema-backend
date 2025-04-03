from typing import Annotated

from fastapi import Depends, Path
from fastapi.requests import Request
from fastapi.routing import APIRouter

from api.v1.cinema.schemas import (
    CreateHallCompleteSchema,
    CreateHallSchema,
    GetHallSchema,
    UpdateHallSchema,
)
from api.v1.cinema.schemas.halls import GetFreeHallPlacesSchema
from apps.cinema.services.halls import BaseHallService
from apps.cinema.use_cases.free_hall_places import GetFreeHallPlaces
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
    hall = await hall_service.get_by_id(id_=id, join_={"rows"})
    return ApiResponse(data=GetHallSchema.to_schema(hall))


@router.patch("/{id}")
async def update_hall_handler(
    request: Request,
    id: Annotated[int, Path(gt=0, description="Enter hall id")],
    update_data: UpdateHallSchema,
    container=Depends(get_container),  # noqa: B008
) -> ApiResponse[CreateHallSchema]:
    hall_service: BaseHallService = container.resolve(BaseHallService)
    hall = await hall_service.update(
        id_=id, attributes=update_data.model_dump(exclude_unset=True)
    )
    return ApiResponse(data=CreateHallSchema.to_schema(hall))


@router.get("/{id}/places")
async def get_free_and_taken_place_hall_per_filmsession(
    request: Request,
    id: Annotated[int, Path(gt=0, description="Enter filmsession id")],
    container=Depends(get_container),  # noqa: B008
) -> ApiResponse[GetFreeHallPlacesSchema]:
    hall_use_case: GetFreeHallPlaces = container.resolve(GetFreeHallPlaces)
    hall, taken_places = await hall_use_case.execute(filmsession_id=id)
    return ApiResponse(
        data=GetFreeHallPlacesSchema.to_schema(
            hall=hall, taken_places=taken_places
        )
    )
