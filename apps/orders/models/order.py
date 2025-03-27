from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import DateTime, ForeignKey, Integer, String, func
from sqlalchemy import Enum as SQLEnum
from sqlalchemy.orm import Mapped, mapped_column, relationship

from apps.orders.models.ticket import Ticket
from core.database import Base
from core.database.mixins import IntegerIdMixin
from core.enums.orders import OrderPaymentStatusEnum

if TYPE_CHECKING:
    from apps.users.models.users import User


class Order(Base, IntegerIdMixin):
    __tablename__ = "orders"

    user_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("users.id", onupdate="CASCADE", ondelete="SET NULL"),
        nullable=True,
    )
    email: Mapped[str] = mapped_column(String(255), nullable=True)
    session_id: Mapped[int] = mapped_column(
        ForeignKey("filmsessions.id", onupdate="CASCADE", ondelete="SET NULL")
    )
    place_id: Mapped[int] = mapped_column(
        ForeignKey("places.id", onupdate="CASCADE", ondelete="SET NULL")
    )
    create_time: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False, default=func.now()
    )
    payment_status: Mapped[OrderPaymentStatusEnum] = mapped_column(
        SQLEnum(OrderPaymentStatusEnum),
        default=OrderPaymentStatusEnum.NOT_PAID,
    )
    user: Mapped["User"] = relationship("User", back_populates="orders")
    ticket: Mapped["Ticket"] = relationship(back_populates="order")
