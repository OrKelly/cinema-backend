from typing import TYPE_CHECKING

from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.types import Enum

from apps.users.models.association_tables import user_genre_association
from core.database import Base
from core.database.mixins import IntegerIdMixin, TimeStampMixin
from core.enums.users import RoleKindEnum

# условие для обхода цикличного импорта
# (либо можно убрать взаимосвязь от user к genre)
if TYPE_CHECKING:
    from apps.films.models import Genre


class User(Base, IntegerIdMixin, TimeStampMixin):
    __tablename__ = "users"

    first_name: Mapped[str] = mapped_column(String(255), nullable=False)
    last_name: Mapped[str] = mapped_column(String(255), nullable=False)
    patronymic: Mapped[str] = mapped_column(String(255), nullable=True)
    password: Mapped[str] = mapped_column(String(255), nullable=False)
    email: Mapped[str] = mapped_column(
        String(255), nullable=False, unique=True
    )
    role: Mapped[RoleKindEnum] = mapped_column(
        Enum(RoleKindEnum), default=RoleKindEnum.CLIENT, nullable=False
    )
    genres: Mapped[list["Genre"]] = relationship(
        argument="Genre",
        secondary=user_genre_association,
        back_populates="users",
    )
    __mapper_args__ = {"eager_defaults": True}
