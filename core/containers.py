from functools import lru_cache

import punq

from apps.cinema.models.halls import Hall
from apps.cinema.models.places import Place
from apps.cinema.models.rows import Row
from apps.cinema.repositories.halls import (
    BaseHallRepository,
    ORMHallRepository,
)
from apps.cinema.repositories.places import (
    BasePlaceRepository,
    ORMPlaceRepository,
)
from apps.cinema.repositories.rows import BaseRowRepository, ORMRowRepository
from apps.cinema.services.halls import (
    BaseHallService,
    BaseHallValidatorService,
    ORMHallService,
    UniqueTitleHallValidatorService,
)
from apps.cinema.services.places import (
    BasePlaceService,
    BasePlaceValidatorService,
    ORMPlaceService,
    PlaceAlreadyExistsValidator,
)
from apps.cinema.services.rows import (
    BaseRowService,
    BaseRowValidatorService,
    ORMRowService,
    RowAlreadyExistsValidator,
)
from apps.cinema.use_cases.hall_create import CreateHallUseCase
from apps.cinema.use_cases.place_create import CreatePlaceUseCase
from apps.cinema.use_cases.row_create import CreateRowUseCase
from apps.films.models.films import Film
from apps.films.repositories.films import (
    BaseFilmRepository,
    BaseORMRepository,
)
from apps.films.services.films import BaseFilmService, ORMFilmService
from apps.films.services.validation import (
    BaseFilmValidatorService,
    FilmRentDatesValidatorService,
)
from apps.films.use_cases.film_create import (
    CreateFilmUseCase,
)
from apps.users.models.users import User
from apps.users.repositories.users import BaseUserRepository, ORMUserRepository
from apps.users.services.register import (
    BaseRegisterValidatorService,
    ComposedRegisterValidatorService,
    PasswordIncorrectValidatorService,
    UniqueEmailValidatorService,
)
from apps.users.services.users import BaseUserService, ORMUserService
from apps.users.use_cases.auth import (
    BaseAuthUserUseCase,
    JwtBasedAuthUserUseCase,
)
from apps.users.use_cases.register import (
    BaseRegisterUserUseCase,
    RegisterUserUseCase,
)
from core.loggers import FileLogger
from core.loggers.base import BaseLogger
from core.storages.s3.base import BaseS3Storage
from core.storages.s3.minio import MinioS3Storage


@lru_cache(1)
def get_container() -> punq.Container:
    return _initialize_container()


def _initialize_storage(container: punq.Container) -> None:
    container.register(BaseS3Storage, MinioS3Storage)


def _initialize_repositories(container: punq.Container) -> None:
    container.register(BaseUserRepository, ORMUserRepository, model_class=User)
    container.register(BaseHallRepository, ORMHallRepository, model_class=Hall)
    container.register(BaseRowRepository, ORMRowRepository, model_class=Row)
    container.register(
        BasePlaceRepository, ORMPlaceRepository, model_class=Place
    )
    container.register(BaseFilmRepository, BaseORMRepository, model_class=Film)


def _initialize_services(container: punq.Container) -> None:
    def build_user_validators() -> BaseRegisterValidatorService:
        return ComposedRegisterValidatorService(
            validators=[
                container.resolve(UniqueEmailValidatorService),
                container.resolve(PasswordIncorrectValidatorService),
            ],
        )

    container.register(UniqueEmailValidatorService)
    container.register(PasswordIncorrectValidatorService)
    container.register(FilmRentDatesValidatorService)
    container.register(BaseUserService, ORMUserService)
    container.register(
        BaseRegisterValidatorService, factory=build_user_validators
    )
    container.register(BaseRowService, ORMRowService)
    container.register(BaseRowValidatorService, RowAlreadyExistsValidator)
    container.register(BaseHallService, ORMHallService)
    container.register(
        BaseRegisterValidatorService, factory=build_user_validators
    )
    container.register(
        BaseHallValidatorService, UniqueTitleHallValidatorService
    )
    container.register(BaseHallService, ORMHallService)
    container.register(BaseFilmService, ORMFilmService)
    container.register(BaseFilmValidatorService, FilmRentDatesValidatorService)
    container.register(BasePlaceService, ORMPlaceService)
    container.register(BasePlaceValidatorService, PlaceAlreadyExistsValidator)


def _initialize_use_cases(container: punq.Container) -> None:
    container.register(RegisterUserUseCase)
    container.register(BaseRegisterUserUseCase, RegisterUserUseCase)
    container.register(BaseAuthUserUseCase, JwtBasedAuthUserUseCase)
    container.register(CreateFilmUseCase)
    container.register(CreateHallUseCase)
    container.register(CreateRowUseCase)
    container.register(CreatePlaceUseCase)


def _initialize_external_staff(container: punq.Container) -> None:
    container.register(BaseLogger, FileLogger)


def _initialize_container() -> punq.Container:
    container = punq.Container()

    _initialize_storage(container)
    _initialize_repositories(container)
    _initialize_services(container)
    _initialize_use_cases(container)
    _initialize_external_staff(container)

    return container
