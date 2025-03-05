from fastapi import Depends
from fastapi.requests import Request
from fastapi.routing import APIRouter

from api.v1.employees.schemas import (
    EmployeeRegisterCompleteSchema,
    EmployeeRegisterSchema,
)
from apps.users.use_cases.register import (
    RegisterEmployeeUseCase,
)
from core.containers import get_container
from core.permissions.base import AdminPermission
from core.permissions.depends import permissions
from core.schemas.responses.api_response import ApiResponse

router = APIRouter()


@router.post("")
async def employee_register_handler(
    request: Request,
    user_data: EmployeeRegisterSchema,
    container=Depends(get_container),  # noqa: B008
    permission=permissions([AdminPermission]),  # noqa: B008
) -> ApiResponse[EmployeeRegisterCompleteSchema]:
    use_case: RegisterEmployeeUseCase = container.resolve(
        RegisterEmployeeUseCase
    )
    employee = await use_case.execute(user_data=user_data.model_dump())
    return ApiResponse(data=EmployeeRegisterCompleteSchema(id=employee.id))
