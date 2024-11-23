from typing import TypeVar

from core.database import Base

ModelType = TypeVar("ModelType", bound=Base)
S3ClientType = TypeVar("S3ClientType")
