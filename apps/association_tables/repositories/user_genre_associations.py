from abc import abstractmethod
from dataclasses import dataclass

from apps.association_tables.models.user_genre_association import (
    user_genre_association,
)
from core.repositories.base import BaseORMRepository


@dataclass
class BaseUserGenreAssociationRepository:
    @abstractmethod
    async def insert_user_genre_association(
        self, user_id: int, genre_ids: list[int]
    ): ...


@dataclass
class ORMUserGenreAssociationRepository(
    BaseUserGenreAssociationRepository,
    BaseORMRepository[user_genre_association],
):
    async def insert_user_genre_association(
        self, user_id: int, genre_ids: list[int]
    ):
        insert_values = [
            {"user_id": user_id, "genre_id": genre_id}
            for genre_id in genre_ids
        ]
        return await super(
            BaseUserGenreAssociationRepository, self
        ).insert_association_table(insert_values=insert_values)
