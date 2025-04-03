from typing import Optional

from pydantic import BaseModel, Field

from apps.cinema.models import Place


class CreatePlaceSchema(BaseModel):
    row_id: int
    number: int


class CreatePlaceCompleteSchema(BaseModel):
    id: int
    row: int
    number: int
    status: str = Field(
        default="Новое место успешно зарегистрировано в базе данных"
    )


class GetPlaceSchema(BaseModel):
    id: int
    number: int

    @classmethod
    def to_schema(cls, place: Place) -> "GetPlaceSchema":
        return cls(id=place.id, number=place.number)


class GetFreePlaceSchema(BaseModel):
    id: int
    number: int
    is_free: Optional[bool] = True

    @classmethod
    def to_schema(
        cls, place: Place, taken_places: set
    ) -> "GetFreePlaceSchema":
        if place.id in taken_places:
            return cls(id=place.id, number=place.number, is_free=False)
        return cls(id=place.id, number=place.number, is_free=True)
