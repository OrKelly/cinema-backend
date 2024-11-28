from typing import List, TYPE_CHECKING
from datetime import datetime

from sqlalchemy import Integer, String, Text, Float, ForeignKey, DateTime
from sqlalchemy import Enum as SQLEnum
from sqlalchemy.orm import Mapped, mapped_column, relationship

from core.database.mixins.id import IntegerIdMixin
from core.database.base import Base
from core.enums.films import AgeRatingEnum, FilmStatusEnum

# условие для обхода цикличного импорта
# (либо можно убрать взаимосвязь от жанра к фильму)
if TYPE_CHECKING:
    from film_sessions import FilmSession
    from apps.films.models.genres import Genre
    from apps.cinema.models.halls import Hall


class Film(Base, IntegerIdMixin):
    __tablename__ = 'films'

    cinemahall_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey('halls.id_hall', onupdate='CASCADE', ondelete='SET NULL'),
    )
    title: Mapped[str] = mapped_column(String(45))
    description: Mapped[str] = mapped_column(Text)
    poster: Mapped[str] = mapped_column(String(255))
    age_rating: Mapped[AgeRatingEnum] = mapped_column(
        SQLEnum(AgeRatingEnum)
    )
    duration: Mapped[float] = mapped_column(Float)
    status: Mapped[FilmStatusEnum] = mapped_column(SQLEnum(FilmStatusEnum))
    date_rent_start: Mapped[datetime] = mapped_column(DateTime(timezone=True))
    date_rent_end: Mapped[datetime] = mapped_column(DateTime(timezone=True))

    genres: Mapped[List['Genre']] = relationship(
        'Genre',
        secondary='film_genre_association',
        back_populates='films'
    )
    halls: Mapped[List['Hall']] = relationship(
        'Hall',
        back_populates='film'
    )
    filmsessions: Mapped[List['FilmSession']] = relationship(
        'FilmSession',
        back_populates='film'
    )
