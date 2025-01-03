from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.types import ASGIApp, Receive, Scope, Send

from core.containers import get_container
from core.loggers.base import BaseLogger


class LoggingMiddleware(BaseHTTPMiddleware):
    def __init__(self, app: ASGIApp) -> None:
        super().__init__(app)

    async def __call__(
        self, scope: Scope, receive: Receive, send: Send
    ) -> None:
        container = get_container()
        logger: BaseLogger = container.resolve(
            BaseLogger, module_name="requests"
        )
        receive_ = await receive()
        request = Request(scope, receive=receive_)

        logger.info(
            f'Request: "{request.method} {request.url}", '
            f'Headers: "{request.headers}" |'
            f" Params: {request.path_params} {request.query_params}",
        )

        await self.app(scope, receive_, send)
