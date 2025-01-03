from pydantic import BaseModel, Field


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
