from sqlalchemy import ForeignKey, Table, Column

from core.database.base import Base


film_genre_association = Table(
    'film_genre_association',
    Base.metadata,
    Column('film_id', ForeignKey('films.id'), primary_key=True),
    Column('genre_id', ForeignKey('genres.id'), primary_key=True)
)
