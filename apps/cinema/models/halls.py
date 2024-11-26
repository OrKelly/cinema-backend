from typing import TYPE_CHECKING

from sqlalchemy import Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from core.database.base import Base

# условие для обхода цикличного импорта
# (либо можно убрать relationship от зала к фильму)
if TYPE_CHECKING:
    from films import Film


class Hall(Base):
    __tablename__ = 'halls'
    id_hall: Mapped[int] = mapped_column(Integer, primary_key=True)
    title: Mapped[str] = mapped_column(String(45))
    description: Mapped[str] = mapped_column(Text)

    film: Mapped['Film'] = relationship(
        'Film',
        back_populates='halls'
    )
