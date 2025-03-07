from typing import Annotated

from fastapi import Depends, Path
from fastapi.requests import Request
from fastapi.routing import APIRouter

from api.v1.cinema.schemas.rows import (
    CreateRowCompleteSchema,
    CreateRowSchema,
    GetRowSchema,
)
from apps.cinema.services.rows import BaseRowService
from apps.cinema.use_cases.row_create import CreateRowUseCase
from core.containers import get_container
from core.schemas.responses.api_response import ApiResponse

router = APIRouter()


@router.post("")
async def create_row_handler(
    request: Request,
    row_schema: CreateRowSchema,
    container=Depends(get_container),  # noqa: B008
) -> ApiResponse[CreateRowCompleteSchema]:
    use_case: CreateRowUseCase = container.resolve(CreateRowUseCase)
    row_data = row_schema.model_dump()
    row = await use_case.execute(row_data)
    return ApiResponse(
        data=CreateRowCompleteSchema(
            id=row.id, number=row.number, capacity=row.capacity
        )
    )


@router.get("/{id}")
async def get_row_handler(
    request: Request,
    id: Annotated[int, Path(gt=0, description="Enter row id")],
    container=Depends(get_container),  # noqa: B008
) -> ApiResponse[GetRowSchema]:
    row_service: BaseRowService = container.resolve(BaseRowService)
    row = await row_service.get_by_id(id_=id, join_={"places"})
    return ApiResponse(data=GetRowSchema.to_schema(row))
