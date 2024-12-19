from pydantic import BaseModel, Field


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
