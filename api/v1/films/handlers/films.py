from fastapi import Depends, UploadFile
from fastapi.requests import Request
from fastapi.routing import APIRouter

from api.v1.films.schemas.films import AddFilmCompleteSchema, FilmAddSchema
from core.containers import get_container
from core.schemas.responses.api_response import ApiResponse
from apps.films.use_cases.film_create import BaseCreateFilmUseCase

router = APIRouter()


@router.post("")
async def create_film_handler(
    request: Request,
    poster: UploadFile,
    film_data: FilmAddSchema,
    container=Depends(get_container),   # noqa: B008
) -> ApiResponse[AddFilmCompleteSchema]:
    use_case: BaseCreateFilmUseCase = container.resolve(
        BaseCreateFilmUseCase
    )
    film_data = film_data.model_dump()
    film = await use_case.execute(film_data=film_data, poster=poster)
    return ApiResponse(
        data=AddFilmCompleteSchema(id=film.id, status="Фильм в базе данных")
    )
