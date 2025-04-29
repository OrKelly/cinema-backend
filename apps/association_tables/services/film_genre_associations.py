from abc import abstractmethod
from dataclasses import dataclass

from apps.association_tables.repositories.film_genre_associations import (
    BaseFilmGenreAssociationRepository,
)
from core.services.base import BaseOrmService


@dataclass
class BaseFilmGenreAssociationService:
    repository: BaseFilmGenreAssociationRepository

    @abstractmethod
    async def insert_film_genre_association(
        self, film_id: int, genre_ids: list[int]
    ): ...


@dataclass
class ORMFilmGenreAssociationService(
    BaseFilmGenreAssociationService, BaseOrmService
):
    async def insert_film_genre_association(
        self, film_id: int, genre_ids: list[int]
    ):
        if genre_ids:
            return await self.repository.insert_film_genre_association(
                film_id=film_id, genre_ids=list(set(genre_ids))
            )
        return genre_ids
