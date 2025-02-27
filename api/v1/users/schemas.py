from collections.abc import Iterable

from pydantic import BaseModel, EmailStr, Field

from apps.users.models.users import User


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


class GetUserSchema(BaseModel):
    id: int
    first_name: str
    last_name: str
    patronymic: str
    email: str
    role: str

    @classmethod
    def to_schema(cls, user: User) -> "GetUserSchema":
        return cls(
            id=user.id,
            first_name=user.first_name,
            last_name=user.last_name,
            patronymic=user.patronymic,
            email=user.email,
            role=user.role.value[1],
        )


class GetAllUsersSchema(BaseModel):
    users: Iterable[GetUserSchema]

    @classmethod
    def to_schema(cls, users_list: Iterable[User]) -> "GetAllUsersSchema":
        return cls(
            users=[GetUserSchema.to_schema(user) for user in users_list]
        )
