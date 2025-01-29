from typing import Annotated

from pydantic import AfterValidator, BaseModel

from api.v1.cinema.schemas.rows import GetRowSchema
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
