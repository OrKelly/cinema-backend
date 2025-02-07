from typing import Annotated

from fastapi import Depends, Path
from fastapi.requests import Request
from fastapi.routing import APIRouter

from api.v1.films.schemas.film_sessions import GetSessionsByFilmID
from api.v1.films.schemas.films import AddFilmCompleteSchema, FilmAddSchema
from apps.films.services.film_sessions import BaseFilmSessionService
from apps.films.use_cases.film_create import CreateFilmUseCase
from core.containers import get_container
from core.schemas.responses.api_response import ApiResponse

router = APIRouter()


@router.post("/")
async def create_film_handler(
    request: Request,
    form_data: FilmAddSchema = Depends(FilmAddSchema.as_form),  # noqa: B008
    container=Depends(get_container),  # noqa: B008
) -> ApiResponse[AddFilmCompleteSchema]:
    use_case: CreateFilmUseCase = container.resolve(CreateFilmUseCase)
    film_data = form_data.model_dump()
    film = await use_case.execute(film_data=film_data)
    return ApiResponse(
        data=AddFilmCompleteSchema(id=film.id, status="Фильм в базе данных")
    )


@router.get("/{id}/sessions")
async def get_film_sessions(
    request: Request,
    id: Annotated[
        int,
        Path(gt=0, description="Введите id фильма, для получения его сеансов"),
    ],
    container=Depends(get_container),  # noqa: B008
) -> ApiResponse[GetSessionsByFilmID]:
    film_session_service: BaseFilmSessionService = container.resolve(
        BaseFilmSessionService
    )
    film_sessions = await film_session_service.get_sessions_by_film_id(
        film_id=id
    )
    return ApiResponse(data=GetSessionsByFilmID.to_schema(film_sessions))
