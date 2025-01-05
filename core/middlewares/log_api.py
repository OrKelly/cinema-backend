from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware

from core.containers import get_container
from core.loggers.base import BaseLogger


class LoggingMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        container = get_container()

        logger: BaseLogger = container.resolve(
            BaseLogger, module_name="requests"
        )

        response = await call_next(request)

        logger.info(
            f'Request: "{request.method} {request.url}", '
            f" Params: {request.path_params} {request.query_params}",
        )

        return response
