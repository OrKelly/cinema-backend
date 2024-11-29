from enum import Enum


class AgeRatingEnum(Enum):
    NO_RESTRICTION = (1, "Без ограничений, 0+")
    KIDS = (2, "6+")
    TEEN = (3, "12+")
    YOUNG = (4, "16+")
    ADULT = (5, "18+")


class FilmStatusEnum(Enum):
    IN_RENT = (1, "В прокате")
    ANNOUNCEMENT = (2, "Анонс")
