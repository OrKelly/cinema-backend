from typing import Self

from pydantic import BaseModel, EmailStr, Field, model_validator

from apps.users.exceptions.auth import NoDataInFieldException


class NewEmployeeRegisterSchema(BaseModel):
    first_name: str
    last_name: str
    patronymic: str = None
    email: EmailStr


class EmployeeRegisterSchema(BaseModel):
    user_id: int = None
    employee_data: NewEmployeeRegisterSchema | None = None

    @model_validator(mode="after")
    def employee_data_validator(self) -> Self:
        if not self.user_id and not self.employee_data:
            raise NoDataInFieldException
        if self.user_id:
            self.employee_data = None
        return self


class EmployeeRegisterCompleteSchema(BaseModel):
    id: int
    status: str = Field(default="Сотрудник успешно зарегистрирован")
