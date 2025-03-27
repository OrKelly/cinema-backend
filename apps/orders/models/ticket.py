from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey, Integer, String, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from core.database import Base
from core.database.mixins import IntegerIdMixin

if TYPE_CHECKING:
    from apps.orders.models.order import Order


class Ticket(Base, IntegerIdMixin):
    __tablename__ = "tickets"

    order_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("orders.id", onupdate="CASCADE", ondelete="CASCADE"),
        nullable=False,
    )
    file: Mapped[str] = mapped_column(String(255), nullable=True)

    order: Mapped["Order"] = relationship(
        back_populates="ticket", single_parent=True
    )

    __table_args__ = (UniqueConstraint("order_id"),)
