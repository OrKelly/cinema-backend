from fastapi import Depends
from fastapi.requests import Request
from fastapi.routing import APIRouter

from api.v1.films.schemas.film_sessions import (
    AddFilmSessionCompleteSchema,
    FilmSessionAddSchema,
)
from apps.films.use_cases.film_session_create import CreateFilmSessionUseCase
from core.containers import get_container
from core.schemas.responses.api_response import ApiResponse

router = APIRouter()


@router.post("")
async def create_film_session_handler(
    request: Request,
    session_data: FilmSessionAddSchema,  # noqa: B008
    container=Depends(get_container),  # noqa: B008
) -> ApiResponse[AddFilmSessionCompleteSchema]:
    use_case: CreateFilmSessionUseCase = container.resolve(
        CreateFilmSessionUseCase
    )
    session_data = session_data.model_dump()
    session = await use_case.execute(attributes=session_data)
    return ApiResponse(data=AddFilmSessionCompleteSchema(id=session.id))
