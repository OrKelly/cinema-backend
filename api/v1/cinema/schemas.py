from pydantic import BaseModel, Field


class CreateHallSchema(BaseModel):
    title: str
    description: str


class CreateHallCompleteSchema(BaseModel):
    id: int
    status: str = Field(
        default="Новый кинозал успешно зарегистрирован в базе данных"
    )
