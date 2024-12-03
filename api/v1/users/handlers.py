from fastapi import Depends
from fastapi.requests import Request
from fastapi.routing import APIRouter

from api.v1.users.schemas import (
    UserLoginSchema,
    UserRegisterCompleteSchema,
    UserRegisterSchema,
)
from apps.users.use_cases.auth import BaseAuthUserUseCase
from apps.users.use_cases.register import BaseRegisterUserUseCase
from core.containers import get_container
from core.schemas.extras.auth import Token
from core.schemas.responses.api_response import ApiResponse

router = APIRouter()


@router.post("/register")
async def user_register_handler(
    request: Request,
    user_data: UserRegisterSchema,
    container=Depends(get_container),  # noqa: B008
) -> ApiResponse[UserRegisterCompleteSchema]:
    use_case: BaseRegisterUserUseCase = container.resolve(
        BaseRegisterUserUseCase
    )
    user_data = user_data.model_dump()
    user = await use_case.execute(user_data=user_data)
    return ApiResponse(
        data=UserRegisterCompleteSchema(
            id=user.id, status="Вы успешно зарегистрированы"
        )
    )


@router.post(
    "/login",
)
async def user_login_handler(
    request: Request,
    credentials_data: UserLoginSchema,
    container=Depends(get_container),  # noqa: B008
) -> ApiResponse[Token]:
    use_case: BaseAuthUserUseCase = container.resolve(BaseAuthUserUseCase)
    credentials_data = credentials_data.model_dump()
    tokens = await use_case.execute(credentials_data=credentials_data)
    return ApiResponse(data=tokens)
