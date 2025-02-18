from fastapi import Depends
from fastapi.requests import Request
from fastapi.routing import APIRouter

from api.v1.films.schemas.genres import GetGenreSchema
from apps.films.services.genres import BaseGenreService
from core.containers import get_container
from core.schemas.responses.api_response import ApiResponse

router = APIRouter()


@router.get("")
async def get_genres_handler(
    request: Request,
    container=Depends(get_container)
 ) -> ApiResponse[list[GetGenreSchema]]:
     genres_servise: BaseGenreService = container.resolve(BaseGenreService)
     genres = await genres_servise.get_all()
     genres_data = [GetGenreSchema.to_schema(genre) for genre in genres]
     return ApiResponse(data=genres_data)
