from typing import TypeVar

from core.database import Base

ModelType = TypeVar("ModelType", bound=Base)
