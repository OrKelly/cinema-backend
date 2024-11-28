from typing import TYPE_CHECKING

from sqlalchemy import Integer, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from core.database.mixins.id import IntegerIdMixin
from core.database.base import Base

# условие для обхода цикличного импорта
# (либо можно убрать взаимосвязь от жанра к фильму)
if TYPE_CHECKING:
    from rows import Row


class Place(Base, IntegerIdMixin):
    __tablename__ = 'places'

    row_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey('rows.id_row', onupdate='CASCADE', ondelete='CASCADE'),
        nullable=False
    )
    number: Mapped[int] = mapped_column(Integer, nullable=False)

    row: Mapped['Row'] = relationship('Row', back_populates='places')
