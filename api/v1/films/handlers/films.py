from datetime import datetime

from fastapi import Depends, UploadFile, Form, File
from fastapi.requests import Request
from fastapi.routing import APIRouter
# from fastapi.params import Body

from api.v1.films.schemas.films import AddFilmCompleteSchema, FilmAddSchema
from core.containers import get_container
from core.schemas.responses.api_response import ApiResponse
from apps.films.use_cases.film_create import BaseCreateFilmUseCase
from core.enums.films import AgeRatingEnum, FilmStatusEnum

router = APIRouter()


@router.post("")
async def create_film_handler(
    request: Request,
    poster: UploadFile = File(...),
    cinemahall_id: int = Form(...),
    description: str = Form(...),
    age_rating: AgeRatingEnum = Form(...),
    duration:  float = Form(...),
    status: FilmStatusEnum = Form(...),
    date_rent_start: datetime = Form(...),
    date_rent_end: datetime = Form(...),
    # film_data_check: FilmAddSchema = Body(),
    container=Depends(get_container),   # noqa: B008
) -> ApiResponse[AddFilmCompleteSchema]:
    use_case: BaseCreateFilmUseCase = container.resolve(
        BaseCreateFilmUseCase
    )
    film_data = FilmAddSchema(
        cinemahall_id=cinemahall_id,
        description=description,
        age_rating=age_rating,
        duration=duration,
        status=status,
        date_rent_start=date_rent_start,
        date_rent_end=date_rent_end
    ).model_dump()
    film = await use_case.execute(film_data=film_data, poster=poster)
    return ApiResponse(
        data=AddFilmCompleteSchema(id=film.id, status="Фильм в базе данных")
    )
