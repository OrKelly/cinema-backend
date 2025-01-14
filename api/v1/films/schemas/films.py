from datetime import datetime

from fastapi import File, Form, UploadFile
from pydantic import BaseModel, Field

from core.enums.films import AgeRatingEnum, FilmStatusEnum


class AddFilmCompleteSchema(BaseModel):
    id: int
    status: str = Field(default="Фильм добавлен")


class FilmAddSchema(BaseModel):
    poster: UploadFile
    title: str
    cinemahall_id: int
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
        cinemahall_id: int = Form(...),  # noqa: B008
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
            cinemahall_id=cinemahall_id,
            description=description,
            age_rating=age_rating,
            duration=duration,
            status=status,
            date_rent_start=date_rent_start,
            date_rent_end=date_rent_end,
        )
