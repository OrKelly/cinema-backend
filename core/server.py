from fastapi import FastAPI
from fastapi.middleware import Middleware
from fastapi.middleware.cors import CORSMiddleware
from fastapi.requests import Request
from fastapi.responses import JSONResponse

from api.v1.urls import router as v1_router
from core.exceptions.base import ServerException
from core.middlewares import SQLAlchemyMiddleware
from core.middlewares.auth import AuthBackend, AuthenticationMiddleware
from core.storages.s3 import MinioS3Storage


def init_routers(app_: FastAPI) -> None:
    """Функция для регистрации роутов"""
    app_.include_router(router=v1_router, prefix="/api")


def make_middleware() -> list[Middleware]:
    """Функция для ининциализации middlewares"""
    return [
        Middleware(
            CORSMiddleware,
            allow_origins=["*"],
            allow_credentials=True,
            allow_methods=["*"],
            allow_headers=["*"],
        ),
        Middleware(SQLAlchemyMiddleware),
        Middleware(AuthenticationMiddleware, backend=AuthBackend()),
    ]


def init_listeners(app_: FastAPI) -> None:
    """Функция создаёт слушателя эксепшенов, сыпящихся из приложения и создает
    кастомный респонс с кодом и сообщением ошибки"""

    @app_.exception_handler(ServerException)
    async def custom_exception_handler(request: Request, exc: ServerException):
        return JSONResponse(
            status_code=exc.code,
            content={"error_code": exc.error_code, "message": exc.message},
        )


def init_storages():
    MinioS3Storage()


def create_app():
    app_ = FastAPI(
        title="Cinema Backend",
        version="1.0.0",
        middleware=make_middleware(),
    )
    init_routers(app_=app_)
    init_listeners(app_=app_)
    init_storages()
    return app_


app = create_app()
