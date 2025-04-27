from datetime import datetime

from fastapi import File, Form, UploadFile
from pydantic import BaseModel, Field

from apps.films.models import Film
from core.enums.films import AgeRatingEnum, FilmStatusEnum


class AddFilmCompleteSchema(BaseModel):
    id: int
    status: str = Field(default="Фильм добавлен")


class FilmAddSchema(BaseModel):
    poster: UploadFile
    title: str
    description: str
    age_rating: AgeRatingEnum
    duration: float
    status: FilmStatusEnum
    date_rent_start: datetime
    date_rent_end: datetime

    @classmethod
    def as_form(
        cls,
        poster: UploadFile = File(...),  # noqa: B008
        title: str = Form(...),  # noqa: B008
        description: str = Form(...),  # noqa: B008
        age_rating: AgeRatingEnum = Form(...),  # noqa: B008
        duration: float = Form(...),  # noqa: B008
        status: FilmStatusEnum = Form(...),  # noqa: B008
        date_rent_start: datetime = Form(...),  # noqa: B008
        date_rent_end: datetime = Form(...),  # noqa: B008
    ) -> "FilmAddSchema":
        return cls(
            poster=poster,
            title=title,
            description=description,
            age_rating=age_rating,
            duration=duration,
            status=status,
            date_rent_start=date_rent_start,
            date_rent_end=date_rent_end,
        )


class FilmInfoSchema(BaseModel):
    title: str
    description: str
    poster: str
    age_rating: AgeRatingEnum
    duration: float
    status: FilmStatusEnum
    date_rent_start: datetime
    date_rent_end: datetime

    @classmethod
    def to_schema(cls, film: Film) -> "FilmInfoSchema":
        return cls(
            poster=film.poster,
            title=film.title,
            description=film.description,
            age_rating=film.age_rating,
            duration=film.duration,
            status=film.status,
            date_rent_start=film.date_rent_start,
            date_rent_end=film.date_rent_end,
        )


class FilmDeletedSchema(BaseModel):
    id: int
    status: str = Field(default="Фильм удален")
