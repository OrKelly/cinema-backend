from dataclasses import dataclass
from typing import Any
from fastapi import UploadFile

from apps.films.services.films import BaseFilmService
from apps.films.services.validation import BaseValidationFilmService
from apps.films.models.films import Film
from core.storages.s3.minio import MinioS3Storage
from .poster_create import CreatePosterUseCase

@dataclass
class BaseCreateFilmUseCase:
    film_service: BaseFilmService
    validator: BaseValidationFilmService
    poster_creator: CreatePosterUseCase

    async def execute(self, film_data: dict[str, Any], poster: UploadFile) -> Film: ...


@dataclass
class CreateFilmUseCase(BaseCreateFilmUseCase):

    async def execute(
            self, film_data: dict[str, Any], poster: UploadFile
    ) -> Film:
        film_data = self.poster_creator.execute(film_data, poster)
        self.validator.validate(film_data)
        return await self.film_service.create(attributes=film_data)
