from dataclasses import dataclass
from typing import Any
from fastapi import UploadFile

from apps.films.services.films import BaseFilmService
from apps.films.services.validation import BaseFilmValidatorService
from apps.films.models.films import Film
from core.storages.s3.minio import MinioS3Storage


@dataclass
class BaseCreateFilmUseCase:
    film_service: BaseFilmService
    validator: BaseFilmValidatorService
    poster_creator: MinioS3Storage

    async def execute(
            self, film_data: dict[str, Any], poster: UploadFile
    ) -> Film: ...


@dataclass
class CreateFilmUseCase(BaseCreateFilmUseCase):

    def upload_poster(
            self, poster: UploadFile
    ) -> str:
        self.poster_creator.upload_file(poster, poster.filename)
        return self.poster_creator.get_object(poster.filename).url()

    async def execute(
            self, film_data: dict[str, Any], poster: UploadFile
    ) -> Film:
        poster_url = self.upload_poster(poster)
        film_data['poster'] = poster_url
        self.validator.validate(film_data)
        return await self.film_service.create(attributes=film_data)
