from datetime import datetime

from fastapi import Depends, File, Form, UploadFile
from fastapi.requests import Request
from fastapi.routing import APIRouter

# from fastapi.params import Body
from api.v1.films.schemas.films import AddFilmCompleteSchema, FilmAddSchema
from apps.films.use_cases.film_create import BaseCreateFilmUseCase
from core.containers import get_container
from core.enums.films import AgeRatingEnum, FilmStatusEnum
from core.schemas.responses.api_response import ApiResponse

router = APIRouter()


@router.post("")
async def create_film_handler(
    request: Request,
    poster: UploadFile = File(...),  # noqa: B008
    cinemahall_id: int = Form(...),  # noqa: B008
    description: str = Form(...),  # noqa: B008
    age_rating: AgeRatingEnum = Form(...),  # noqa: B008
    duration: float = Form(...),  # noqa: B008
    status: FilmStatusEnum = Form(...),  # noqa: B008
    date_rent_start: datetime = Form(...),  # noqa: B008
    date_rent_end: datetime = Form(...),  # noqa: B008
    # film_data_check: FilmAddSchema = Body(),
    container=Depends(get_container),  # noqa: B008
) -> ApiResponse[AddFilmCompleteSchema]:
    use_case: BaseCreateFilmUseCase = container.resolve(BaseCreateFilmUseCase)
    film_data = FilmAddSchema(
        cinemahall_id=cinemahall_id,
        description=description,
        age_rating=age_rating,
        duration=duration,
        status=status,
        date_rent_start=date_rent_start,
        date_rent_end=date_rent_end,
    ).model_dump()
    film = await use_case.execute(film_data=film_data, poster=poster)
    return ApiResponse(
        data=AddFilmCompleteSchema(id=film.id, status="Фильм в базе данных")
    )
