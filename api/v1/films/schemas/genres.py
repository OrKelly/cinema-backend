from collections.abc import Iterable

from pydantic import BaseModel

from apps.films.models import Genre


class GetGenreSchema(BaseModel):
    id: int
    title: str

    @classmethod
    def to_schema(cls, genre: Genre) -> "GetGenreSchema":
        return cls(
            id=genre.id,
            title=genre.title,
        )


class GetAllGenresSchema(BaseModel):
    genres: Iterable[GetGenreSchema]

    @classmethod
    def to_schema(cls, genres_list: Iterable[Genre]) -> "GetAllGenresSchema":
        return cls(
            genres=[GetGenreSchema.to_schema(genre) for genre in genres_list]
        )
