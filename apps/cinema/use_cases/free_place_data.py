from dataclasses import dataclass

from apps.cinema.services.halls import BaseHallService
from apps.films.services.film_sessions import BaseFilmSessionService


@dataclass
class GetFreePlaceHall:
    filmsession_service: BaseFilmSessionService
    hals_service: BaseHallService

    async def execute(self, filmsession_id: int):
        filmsession = await self.filmsession_service.get_by_id(
            id_=filmsession_id, join_={"hall"}
        )
        return filmsession.hall
