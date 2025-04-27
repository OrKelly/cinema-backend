from pydantic import BaseModel, Field

from api.v1.cinema.schemas.places import GetFreePlaceSchema, GetPlaceSchema
from apps.cinema.models import Row


class CreateRowSchema(BaseModel):
    hall_id: int
    number: int
    capacity: int


class CreateRowCompleteSchema(BaseModel):
    id: int
    number: int
    capacity: int
    status: str = Field(
        default="Новый ряд успешно зарегистрирован в базе данных"
    )


class GetRowSchema(BaseModel):
    id: int
    number: int
    capacity: int
    places: list[GetPlaceSchema]

    @classmethod
    def to_schema(cls, row: Row) -> "GetRowSchema":
        return cls(
            id=row.id,
            number=row.number,
            capacity=row.capacity,
            places=[GetPlaceSchema.to_schema(place) for place in row.places],
        )


class GetFreeRowPlacesSchema(BaseModel):
    id: int
    number: int
    capacity: int
    places: list[GetFreePlaceSchema]

    @classmethod
    def to_schema(
        cls, row: Row, taken_places: set
    ) -> "GetFreeRowPlacesSchema":
        return cls(
            id=row.id,
            number=row.number,
            capacity=row.capacity,
            places=[
                GetFreePlaceSchema.to_schema(
                    place=place, taken_places=taken_places
                )
                for place in row.places
            ],
        )
