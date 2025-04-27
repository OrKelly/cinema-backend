from typing import Annotated, Optional

from pydantic import AfterValidator, BaseModel

from api.v1.cinema.schemas.rows import GetFreeRowPlacesSchema, GetRowSchema
from apps.cinema.models.halls import Hall


def val_len(value: str) -> str:
    if len(value) > 45:
        raise ValueError("Допустимая длина title не более 45 символов")
    return value


class CreateHallSchema(BaseModel):
    title: Annotated[str, AfterValidator(val_len)]
    description: str

    @classmethod
    def to_schema(cls, hall: Hall) -> "CreateHallSchema":
        return cls(
            title=hall.title,
            description=hall.description,
        )


class CreateHallCompleteSchema(BaseModel):
    id: int
    title: str


class UpdateHallSchema(BaseModel):
    title: Optional[Annotated[str, AfterValidator(val_len)]] = None
    description: Optional[str] = None


class GetHallSchema(BaseModel):
    id: int
    title: str
    description: str
    rows: list[GetRowSchema]

    @classmethod
    def to_schema(cls, hall: Hall) -> "GetHallSchema":
        return cls(
            id=hall.id,
            title=hall.title,
            description=hall.description,
            rows=[GetRowSchema.to_schema(row) for row in hall.rows],
        )


class GetFreeHallPlacesSchema(BaseModel):
    id: int
    title: str
    description: str
    rows: list[GetFreeRowPlacesSchema]

    @classmethod
    def to_schema(
        cls, hall: Hall, taken_places: set
    ) -> "GetFreeHallPlacesSchema":
        return cls(
            id=hall.id,
            title=hall.title,
            description=hall.description,
            rows=[
                GetFreeRowPlacesSchema.to_schema(
                    row=row, taken_places=taken_places
                )
                for row in hall.rows
            ],
        )
