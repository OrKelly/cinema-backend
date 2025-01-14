from pydantic import BaseModel, Field

from api.v1.cinema.schemas.places import GetPlaceSchema
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
