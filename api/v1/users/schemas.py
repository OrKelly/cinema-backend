from pydantic import BaseModel, EmailStr, Field, field_validator

from apps.users.exceptions.auth import InvalidFieldException


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


class NewEmployeeRegisterSchema(BaseModel):
    first_name: str
    last_name: str
    patronymic: str = None
    email: EmailStr


class EmployeeRegisterSchema(BaseModel):
    user_id: int = None
    employee_data: NewEmployeeRegisterSchema = None

    @field_validator('employee_data', mode='before')
    def employee_data_validator(cls, value, info):
        if info.data.get('user_id') is not None:
            raise InvalidFieldException
        return value


class EmployeeRegisterCompleteSchema(BaseModel):
    id: int
    status: str = Field(default="Сотрудник успешно зарегистрирован")
