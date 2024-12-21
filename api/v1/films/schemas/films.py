from datetime import datetime
from pydantic import BaseModel, Field

from core.enums.films import AgeRatingEnum, FilmStatusEnum


class AddFilmCompleteSchema(BaseModel):
    id: int
    status: str = Field(default="Фильм добавлен")


class FilmAddSchema(BaseModel):
    cinemahall_id: int
    description: str
    poster: str
    age_rating: AgeRatingEnum
    duration:  float
    status: FilmStatusEnum
    date_rent_start: datetime
    date_rent_end: datetime
