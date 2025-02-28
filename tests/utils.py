from collections.abc import Iterable
from typing import Callable

from fastapi import FastAPI

from core.permissions.base import BasePermission
from core.permissions.depends import permissions


def create_test_app_with_route(
    app: FastAPI,
    route_path: str,
    permission_classes: Iterable[type[BasePermission]] = None,
    route_method: Callable = None,
) -> FastAPI:
    """Функция для создания фейковых роутов"""

    route_method = route_method or (lambda: {"message": "Hello world"})

    dependencies = []

    if permission_classes:
        dependencies.append(permissions(permission_classes))

    app.add_api_route(
        route_path,
        route_method,
        dependencies=dependencies,
    )
    return app
