from loguru import logger
from fastapi import Request
from starlette.types import ASGIApp, Receive, Scope, Send
from starlette.middleware.base import BaseHTTPMiddleware


class LoggingAPIMiddleware(BaseHTTPMiddleware):  
    def __init__(self, app: ASGIApp) -> None:  
        super().__init__(app)
    
    
    async def __call__(
        self, scope: Scope, receive: Receive, send: Send
        ) -> None:
        receive_ = await receive()
        request = Request(scope, receive=receive_)

        logger.info(
            'Request: "{method} {path}"',
            method=request.method,
            path=request.url,
        )

        logger.bind(
            path=request.url,
            method=request.method
        ).info(
            'Request headers: "{headers}" | Params: {path_param} {query_param}',
            headers=request.headers,
            path_param=request.path_params,
            query_param=request.query_params
        )
        
        await self.app(scope, receive_, send)
        