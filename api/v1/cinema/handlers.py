from fastapi import Depends
from fastapi.routing import APIRouter
from fastapi.requests import Request

from api.v1.cinema.schemas import CreateHallSchema, CreateHallCompleteSchema
from core.containers import get_container
from core.schemas.responses.api_response import ApiResponse
from apps.cinema.repositories.halls import ORMHallRepository, BaseHallsRepository

router = APIRouter()


# @router.post('api/v1/cinema/halls')
# async def create_hall_handler(
#     request: Request,
#     hall_data: CreateHallSchema,
#     container=Depends(get_container),   # noqa: B008
# ) -> ApiResponse[CreateHallCompleteSchema]:
#     repository: ORMHallRepository = container.resolve(BaseHallsRepository)
#     hall_data = hall_data.model_dump()
#     hall = await repository.create()

if __name__ == '__main__':
    container=Depends(get_container)
    repository: ORMHallRepository = container.resolve(BaseHallsRepository)
    print(repository)