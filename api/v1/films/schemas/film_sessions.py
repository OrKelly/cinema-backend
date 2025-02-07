from collections.abc import Iterable
from datetime import datetime

from pydantic import BaseModel, Field

from apps.films.models.film_sessions import FilmSession


class AddFilmSessionCompleteSchema(BaseModel):
    id: int
    status: str = Field(default="Сеанс добавлен")


class FilmSessionAddSchema(BaseModel):
    film_id: int
    date_time: datetime
    price: float


class FilmSessionSchema(BaseModel):
    id: int
    datetime: datetime
    price: float

    @classmethod
    def to_schema(cls, film_session: FilmSession) -> "FilmSessionSchema":
        return cls(
            id=film_session.id,
            datetime=film_session.date_time,
            price=film_session.price,
        )


class GetSessionsByFilmID(BaseModel):
    film_sessions: Iterable[FilmSessionSchema]

    @classmethod
    def to_schema(
        cls, film_session_list: Iterable[FilmSession]
    ) -> "GetSessionsByFilmID":
        return cls(
            film_sessions=[
                FilmSessionSchema.to_schema(film_session)
                for film_session in film_session_list
            ],
        )
