
from pydantic import BaseModel, EmailStr, Field


class UserRegisterSchema(BaseModel):
    first_name: str
    last_name: str
    patronymic: str = None
    password: str
    email: EmailStr


class UserRegisterCompleteSchema(BaseModel):
    id: int
    status: str = Field(default="Вы успешно зарегистрировались")


class UserLoginSchema(BaseModel):
    email: EmailStr
    password: str
