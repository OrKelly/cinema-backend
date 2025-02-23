from typing import TYPE_CHECKING

from sqlalchemy import Boolean, ForeignKey, Integer, String
from sqlalchemy import Enum as SQLEnum
from sqlalchemy.orm import Mapped, mapped_column, relationship

from core.database import Base
from core.database.mixins import IntegerIdMixin
from core.enums.notifications import (
    NotificationKindEnum,
    NotificationSendStatus,
)

if TYPE_CHECKING:
    from apps.users.models.users import User


class Notification(Base, IntegerIdMixin):
    __tablename__ = "notifications"

    user_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("users.id", onupdate="CASCADE", ondelete="SET NULL"),
        nullable=True,
    )
    email: Mapped[str] = mapped_column(String(255), nullable=False)
    title: Mapped[str] = mapped_column(String(100))
    body: Mapped[str] = mapped_column(String(255), nullable=True)
    read_status: Mapped[bool] = mapped_column(Boolean, default=False)
    send_status: Mapped[NotificationSendStatus] = mapped_column(
        SQLEnum(NotificationSendStatus),
        default=NotificationSendStatus.NOT_SENT,
    )
    kind: Mapped[NotificationKindEnum] = mapped_column(
        SQLEnum(NotificationKindEnum)
    )

    user: Mapped["User"] = relationship("User", back_populates="notifications")
