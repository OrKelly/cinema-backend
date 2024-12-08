from pydantic import BaseModel, Field













class CreateRowSchema(BaseModel):
    hall_id: int
    number: int


class CreateRowCompleteSchema(BaseModel):
    id: int
    number: int
    status: str = Field(default="Новый ряд успешно зарегистрирован в базе данных")