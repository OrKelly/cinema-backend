from pydantic import BaseModel

from apps.films.models import Genre


class GetGenreSchema(BaseModel):

    id: int
    title: str

    @classmethod
    def to_schema(cls, genre: Genre) -> "GetGenreSchema":
        return cls(id=genre.id, title=genre.title)
