from dataclasses import dataclass
from typing import Any

from fastapi import UploadFile

from apps.films.models.films import Film
from apps.films.services.films import BaseFilmService
from apps.films.services.validation import BaseFilmValidatorService
from core.storages.s3.base import BaseS3Storage
from core.storages.s3.utils import remove_file_on_exception


@dataclass
class CreateFilmUseCase:
    film_service: BaseFilmService
    validator: BaseFilmValidatorService
    poster_creator: BaseS3Storage

    async def execute(self, film_data: dict[str, Any]) -> Film:
        poster = film_data["poster"]
        async with remove_file_on_exception(
            storage_service=self.poster_creator,
            file_path=f"posters/{poster.filename}",
        ):
            poster_url = self.upload_poster(poster)
            film_data["poster"] = poster_url
            await self.validator.validate(film_data)
            return await self.film_service.create(attributes=film_data)

    def upload_poster(self, poster: UploadFile) -> str:
        poster_filepath = f"posters/{poster.filename}"
        self.poster_creator.upload_file_from_stream(
            poster_filepath, poster.file, poster.size
        )
        return self.poster_creator.get_object(poster_filepath).url
