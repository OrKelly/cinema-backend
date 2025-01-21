from pydantic import BaseModel

from api.v1.cinema.schemas.rows import GetRowSchema
from apps.cinema.models.halls import Hall


class CreateHallSchema(BaseModel):
    title: str
    description: str


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
