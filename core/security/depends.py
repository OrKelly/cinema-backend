from fastapi import Depends
from fastapi.requests import HTTPConnection

from apps.users.models.users import User
from apps.users.services.users import BaseUserService
from core.containers import get_container
from core.schemas.extras.auth import CurrentUser


async def get_current_user(
    conn: HTTPConnection,
    container=Depends(get_container),  # noqa: B008
) -> User | None:
    current_user: CurrentUser = conn.scope.get("user")
    if not conn.scope.get("auth"):
        return None
    service: BaseUserService = container.resolve(BaseUserService)
    return await service.get_by_id(id_=current_user.id)
