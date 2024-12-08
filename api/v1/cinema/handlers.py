from fastapi import Depends
from fastapi.requests import Request
from fastapi.routing import APIRouter

from api.v1.cinema.schemas import CreateRowSchema, CreateRowCompleteSchema
from apps.cinema.services.rows import BaseRowService
from core.containers import get_container
from core.schemas.responses.api_response import ApiResponse

router = APIRouter()


@router.post("/rows")
async def create_row_handler(
    request: Request,
    row_data: CreateRowSchema,
    container=Depends(get_container),  # noqa: B008
) -> ApiResponse[CreateRowCompleteSchema]:
    row_service: BaseRowService = container.resolve(BaseRowService)
    row_data = row_data.model_dump()
    row = await row_service.create(row_data)
    return ApiResponse(data=CreateRowCompleteSchema(id=row.id, number=row.number))
