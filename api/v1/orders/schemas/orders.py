from typing import Self

from pydantic import BaseModel, EmailStr, Field, model_validator


class OrderAddSchema(BaseModel):
    user_id: int | None = None
    email: EmailStr | None = None
    filmsession_id: int
    place_ids: list[int]

    @model_validator(mode="after")
    def check_empty_list(self) -> Self:
        if not self.place_ids:
            raise ValueError("place_ids expected value")
        return self


class OrderCompleteSchema(BaseModel):
    order_ids: list[int]
    status: str = Field(
        default="Бронь прошла успешно! Билеты отправлены на почту"
    )
