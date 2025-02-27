from sqlalchemy import Column, ForeignKey, Table

from core.database.base import Base

user_genre_association = Table(
    "user_genre_association",
    Base.metadata,
    Column("user_id", ForeignKey("users.id"), primary_key=True),
    Column("genre_id", ForeignKey("genres.id"), primary_key=True),
)
