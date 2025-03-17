from pydantic import BaseModel, EmailStr, Field


class OrderAddSchema(BaseModel):
    user_id: int | None = None
    email: EmailStr | None = None
    session_id: int
    place_id: int


class OrderCompleteSchema(BaseModel):
    id: int
    status: str = Field(
        default="Бронь прошла успешно! Билеты отправлены на почту"
    )
