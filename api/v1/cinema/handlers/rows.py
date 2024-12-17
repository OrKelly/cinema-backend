from fastapi import Depends
from fastapi.requests import Request
from fastapi.routing import APIRouter

from api.v1.cinema.schemas.rows import CreateRowCompleteSchema, CreateRowSchema
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
        data=CreateRowCompleteSchema(id=row.id, number=row.number)
    )
