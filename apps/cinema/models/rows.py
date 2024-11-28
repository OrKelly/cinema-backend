from typing import List
from typing import TYPE_CHECKING


from sqlalchemy import Integer, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from core.database.mixins.id import IntegerIdMixin
from core.database.base import Base

# условие для обхода цикличного импорта
# (либо можно убрать взаимосвязь)
if TYPE_CHECKING:
    from places import Place


class Row(Base, IntegerIdMixin):
    __tablename__ = 'rows'

    hall_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey('rows.id_row', onupdate='CASCADE', ndelete='CASCADE'),
        nullable=False
    )
    number: Mapped[int] = mapped_column(Integer, nullable=False)

    places: Mapped[List['Place']] = relationship('Place', back_populates='row')
