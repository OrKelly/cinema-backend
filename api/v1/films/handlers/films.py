from fastapi import Depends
from fastapi.requests import Request
from fastapi.routing import APIRouter

from api.v1.films.schemas.films import AddFilmCompleteSchema, FilmAddSchema
from apps.films.use_cases.film_create import CreateFilmUseCase
from core.containers import get_container
from core.schemas.responses.api_response import ApiResponse

router = APIRouter()


@router.post("")
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
