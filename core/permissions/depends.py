from collections.abc import Iterable
from typing import Any

from fastapi import Depends, status
from fastapi.exceptions import HTTPException
from fastapi.requests import HTTPConnection

from core.permissions.base import BasePermission
from core.schemas.extras.auth import CurrentUser
from core.security.depends import get_current_user


def permissions(
    permissions_classes: Iterable[type[BasePermission]],
) -> Any:
    async def check_permission_wrapper(
        conn: HTTPConnection,
        current_user: CurrentUser = Depends(get_current_user),  # noqa: B008
    ):
        for permission_class in permissions_classes:
            permission = permission_class(user=current_user)
            if not await permission.check_permission(**conn.path_params):
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail="Доступ запрещен",
                )

    return Depends(check_permission_wrapper)
