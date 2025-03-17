from typing import TYPE_CHECKING

from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.types import Enum

from apps.association_tables.models.user_genre_association import (
    user_genre_association,
)
from core.database import Base
from core.database.mixins import IntegerIdMixin, TimeStampMixin
from core.enums.users import RoleKindEnum

if TYPE_CHECKING:
    from apps.films.models import Genre
    from apps.notifications.models.notification import Notification
    from apps.orders.models.order import Order


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

    notifications: Mapped[list["Notification"]] = relationship(
        "Notification", back_populates="user"
    )

    orders: Mapped[list["Order"]] = relationship(
        "Order", back_populates="user"
    )

    @property
    def full_name(self) -> str:
        return f"{self.last_name} {self.first_name} {self.patronymic}"
