from fastapi.routing import APIRouter
from fastapi.requests import Request

from core.schemas.extras.health import HealthSchema
from core.schemas.responses.api_response import ApiResponse

router = APIRouter(
)


@router.get("/health")
def health(request: Request) -> ApiResponse[HealthSchema]:
    return ApiResponse(data=HealthSchema(status="Ok!"))
