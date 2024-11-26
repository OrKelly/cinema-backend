from typing import List, TYPE_CHECKING

from sqlalchemy import Integer, String, Text, Float, ForeignKey
from sqlalchemy import Enum as SQLEnum
from sqlalchemy.orm import Mapped, mapped_column, relationship

from core.database.base import Base
from core.enums.films import AgeRatingEnum, FilmStatusEnum

# условие для обхода цикличного импорта
# (либо можно убрать взаимосвязь от жанра к фильму)
if TYPE_CHECKING:
    from film_sessions import FilmSession
    from apps.films.models.genres import Genre
    from apps.cinema.models.halls import Hall


class Film(Base):
    __tablename__ = 'films'
    id_film: Mapped[int] = mapped_column(Integer, primary_key=True)
    genre_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey('genres.id_genre', ondelete='SET NULL')
    )
    cinemahall_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey('halls.id_hall', ondelete='SET NULL'),
    )
    title: Mapped[str] = mapped_column(String(45))
    description: Mapped[str] = mapped_column(Text)
    poster: Mapped[str] = mapped_column(String(255))
    age_rating: Mapped[AgeRatingEnum] = mapped_column(
        SQLEnum(AgeRatingEnum)
    )
    duration: Mapped[float] = mapped_column(Float)  # здесь в схемах стоял int, думаю нужен float
    status: Mapped[FilmStatusEnum] = mapped_column(SQLEnum(FilmStatusEnum))
    
    genres: Mapped[List['Genre']] = relationship(
        'Genre',
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
