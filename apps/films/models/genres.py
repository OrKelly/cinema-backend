from typing import TYPE_CHECKING, List

from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from core.database.base import Base

# условие для обхода цикличного импорта
# (либо можно убрать взаимосвязь от жанра к фильму)
if TYPE_CHECKING:
    from films import Film


class Genre(Base):
    __tablename__ = 'genres'
    id_genre: Mapped[int] = mapped_column(Integer, primary_key=True)
    title: Mapped[str] = mapped_column(String(45))

    films: Mapped[List['Film']] = relationship(
        'Film',
        back_populates='genres'
    )
