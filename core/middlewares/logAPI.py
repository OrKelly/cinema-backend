from loguru import logger


class LoggingAPIMiddleware:  
    def __init__(self, get_response):  
        self.get_response = get_response  

    def __call__(self, request):
        response = self.get_response(request) 
        logger.bind(
            path=request.path,
            method=request.method,
            status_code=response.status_code,
            response_size=len(response.content),
        ).info(
            'Request: "{method} {path}" | Response: {status_code}',
            method=request.method,
            path=request.path,
            status_code=response.status_code
        )
        return response
