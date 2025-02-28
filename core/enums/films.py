from enum import Enum


class AgeRatingEnum(Enum):
    NO_RESTRICTION = "Без ограничений, 0+"
    KIDS = "6+"
    TEEN = "12+"
    YOUNG = "16+"
    ADULT = "18+"


class FilmStatusEnum(Enum):
    IN_RENT = "В прокате"
    ANNOUNCEMENT = "Анонс"
