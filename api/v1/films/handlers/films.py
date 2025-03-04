from typing import Annotated

from fastapi import Depends, Path
from fastapi.requests import Request
from fastapi.routing import APIRouter

from api.v1.films.schemas.film_sessions import GetSessionsByFilmID
from api.v1.films.schemas.films import (
    AddFilmCompleteSchema,
    FilmAddSchema,
    FilmInfoSchema,
)
from api.v1.films.schemas.genres import GetAllGenresSchema
from apps.films.services.film_sessions import BaseFilmSessionService
from apps.films.services.films import BaseFilmService
from apps.films.services.genres import BaseGenreService
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


@router.get("/genres")
async def get_film_genres(
    request: Request,
    container=Depends(get_container),  # noqa: B008
) -> ApiResponse[GetAllGenresSchema]:
    genre_service: BaseGenreService = container.resolve(BaseGenreService)
    genres = await genre_service.get_all()

    return ApiResponse(data=GetAllGenresSchema.to_schema(genres))


@router.get("/{id}")
async def get_film_by_id(
    request: Request,
    id: Annotated[
        int,
        Path(
            gt=0,
            description="Введите id фильма, для получения информации "
            "о фильме",
        ),
    ],
    container=Depends(get_container),  # noqa: B008
) -> ApiResponse[FilmInfoSchema]:
    film_id_service: BaseFilmService = container.resolve(BaseFilmService)
    film = await film_id_service.get_by_id(id_=id)

    return ApiResponse(data=FilmInfoSchema.to_schema(film))


@router.delete("/{id}")
async def delete_film_by_id(
    request: Request,
    id: Annotated[
        int,
        Path(gt=0, description="Введите id фильма, для удаления"),
    ],
    container=Depends(get_container),  # noqa: B008
):
    film_id_service: BaseFilmService = container.resolve(BaseFilmService)
    film = await film_id_service.get_by_id(id_=id)

    return await film_id_service.delete(film=film)
