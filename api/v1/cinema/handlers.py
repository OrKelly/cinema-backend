from fastapi.requests import Request
from fastapi.routing import APIRouter

from core.schemas.extras.health import HealthSchema
from core.schemas.responses.api_response import ApiResponse

router = APIRouter()


@router.post("/health")
def health(request: Request) -> ApiResponse[HealthSchema]:
    return ApiResponse(data=HealthSchema(status="Ok!"))
