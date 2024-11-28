from typing import TYPE_CHECKING, List

from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from core.database.mixins.id import IntegerIdMixin
from core.database.base import Base

# условие для обхода цикличного импорта
# (либо можно убрать взаимосвязь от жанра к фильму)
if TYPE_CHECKING:
    from films import Film


class Genre(Base, IntegerIdMixin):
    __tablename__ = 'genres'

    title: Mapped[str] = mapped_column(String(45))

    films: Mapped[List['Film']] = relationship(
        'Film',
        secondary='film_genre_association',
        back_populates='genres'
    )
