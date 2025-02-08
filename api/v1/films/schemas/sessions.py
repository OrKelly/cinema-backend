from datetime import datetime

from pydantic import BaseModel, Field


class AddFilmSessionCompleteSchema(BaseModel):
    id: int
    status: str = Field(default="Сеанс добавлен")


class FilmSessionAddSchema(BaseModel):
    film_id: int
    date_time: datetime
    price: float
