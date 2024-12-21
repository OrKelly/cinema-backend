from dataclasses import dataclass
from typing import Any
from fastapi import UploadFile

from apps.films.services.films import BaseFilmService
from apps.films.models.films import Film
from core.storages.s3.minio import MinioS3Storage


@dataclass
class BaseCreatePosterUseCase:
    film_service: BaseFilmService
    s3storage_client: MinioS3Storage

    def execute(
            self, film_data: dict[str, Any], poster: UploadFile
    ) -> Film: ...


@dataclass
class CreatePosterUseCase(BaseCreatePosterUseCase):
    def execute(
            self, film_data: dict[str, Any], poster: UploadFile
    ) -> dict:
        self.s3storage_client.upload_file(poster, poster.filename)
        ref = (
            f"http://{self.s3storage_client.endpoint}/"
            f"{self.s3storage_client.bucket_name}/"
            f"{poster.filename}"
        )
        film_data["poster"] = ref
        return film_data
