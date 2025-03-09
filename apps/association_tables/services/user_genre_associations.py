from abc import abstractmethod
from dataclasses import dataclass

from apps.association_tables.repositories.user_genre_associations import (
    BaseUserGenreAssociationRepository,
)
from apps.users.services.users import BaseUserService
from core.services.base import BaseOrmService


@dataclass
class BaseUserGenreAssociationService:
    repository: BaseUserGenreAssociationRepository
    user_service: BaseUserService

    @abstractmethod
    async def insert_user_genre_association(
        self, user_id: int, genre_ids: list[int]
    ): ...


@dataclass
class ORMUserGenreAssociationService(
    BaseUserGenreAssociationService, BaseOrmService
):
    async def insert_user_genre_association(
        self, user_id: int, genre_ids: list[int]
    ):
        user = await self.user_service.get_by_id(id_=user_id, join_={"genres"})
        new_genre_ids = list(
            set(genre_ids) - set(map(lambda item: item.id, user.genres))
        )
        if new_genre_ids:
            return await self.repository.insert_user_genre_association(
                user_id=user_id, genre_ids=genre_ids
            )
        return genre_ids
