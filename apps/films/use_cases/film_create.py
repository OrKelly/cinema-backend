
import tempfile
import shutil
import os

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
        with tempfile.NamedTemporaryFile(delete=False) as temp_file:
            shutil.copyfileobj(poster.file, temp_file)
            temp_file_path = temp_file.name
        try:
            self.poster_creator.upload_file(temp_file_path, poster.filename)
            print(self.poster_creator.get_object(poster.filename))
            # return self.poster_creator.get_object(poster.filename).url()
        finally:
            os.remove(temp_file_path)

    async def execute(
            self, film_data: dict[str, Any], poster: UploadFile
    ) -> Film:
        poster_url = self.upload_poster(poster)
        result_data = film_data.copy()
        result_data['poster'] = poster_url
        self.validator.validate(result_data)
        print(f"Перед сохранением: {film_data}")
        film = await self.film_service.create(attributes=film_data)
        print(f"После сохранения: {film}")
        return film
