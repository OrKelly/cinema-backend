from typing import List
from typing import TYPE_CHECKING


from sqlalchemy import Integer, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from core.database.base import Base

# условие для обхода цикличного импорта
# (либо можно убрать взаимосвязь)
if TYPE_CHECKING:
    from places import Place


class Row(Base):
    __tablename__ = 'rows'
    id_row: Mapped[int] = mapped_column(Integer, primary_key=True)
    hall_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey('rows.id_row', ondelete='CASCADE'),
        nullable=False
    )
    number: Mapped[int] = mapped_column(Integer, nullable=False)

    places: Mapped[List['Place']] = relationship('Place', back_populates='row')
