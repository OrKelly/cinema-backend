from dataclasses import dataclass

from apps.cinema.models import Hall
from apps.cinema.services.halls import BaseHallService
from apps.films.services.film_sessions import BaseFilmSessionService
from apps.orders.services.orders import BaseOrderService


@dataclass
class GetFreeHallPlaces:
    filmsession_service: BaseFilmSessionService
    hals_service: BaseHallService
    order_service: BaseOrderService

    async def execute(self, filmsession_id: int) -> tuple[Hall, set]:
        filmsession = await self.filmsession_service.get_by_id(
            id_=filmsession_id, join_={"hall"}
        )
        orders = await self.order_service.get_by_filter(
            filter_params={"filmsession_id": filmsession_id}
        )
        taken_places = {order.place_id for order in orders}
        hall = await self.hals_service.get_by_id(
            id_=filmsession.hall_id, join_={"rows"}
        )

        return hall, taken_places
