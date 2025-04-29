from abc import abstractmethod
from dataclasses import dataclass

from apps.association_tables.models.film_genre_association import (
    film_genre_association,
)
from core.repositories.base import BaseORMRepository


@dataclass
class BaseFilmGenreAssociationRepository:
    @abstractmethod
    async def insert_film_genre_association(
        self, film_id: int, genre_ids: list[int]
    ): ...


@dataclass
class ORMFilmGenreAssociationRepository(
    BaseFilmGenreAssociationRepository,
    BaseORMRepository[film_genre_association],
):
    async def insert_film_genre_association(
        self, film_id: int, genre_ids: list[int]
    ):
        insert_values = [
            {"film_id": film_id, "genre_id": genre_id}
            for genre_id in genre_ids
        ]
        return await super(
            BaseFilmGenreAssociationRepository, self
        ).insert_association_table(insert_values=insert_values)
