from functools import lru_cache

import punq

from apps.association_tables.models import user_genre_association
from apps.association_tables.repositories.user_genre_associations import (
    BaseUserGenreAssociationRepository,
    ORMUserGenreAssociationRepository,
)
from apps.association_tables.services.user_genre_associations import (
    BaseUserGenreAssociationService,
    ORMUserGenreAssociationService,
)
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
from apps.films.models import FilmSession
from apps.films.models.films import Film
from apps.films.models.genres import Genre
from apps.films.repositories.film_sessions import (
    BaseFilmSessionRepository,
    ORMFilmSessionRepository,
)
from apps.films.repositories.films import (
    BaseFilmRepository,
    ORMFilmRepository,
)
from apps.films.repositories.genres import (
    BaseGenreRepository,
    ORMGenreRepository,
)
from apps.films.services.film_sessions import (
    BaseFilmSessionService,
    BaseFilmSessionValidatorService,
    ComposedFilmSessionValidator,
    FilmSessionIsDateTimeFreeValidatorService,
    FilmSessionValidatorService,
    ORMFilmSessionService,
)
from apps.films.services.films import BaseFilmService, ORMFilmService
from apps.films.services.genres import BaseGenreService, ORMGenreService
from apps.films.services.validation import (
    BaseFilmValidatorService,
    FilmRentDatesValidatorService,
)
from apps.films.use_cases.film_create import (
    CreateFilmUseCase,
)
from apps.films.use_cases.film_session_create import CreateFilmSessionUseCase
from apps.notifications.models.notification import Notification
from apps.notifications.repositories.notification import (
    BaseNotificationRepository,
    ORMNotificationRepository,
)
from apps.notifications.services.send_services.base import (
    BaseNotificationService,
)
from apps.notifications.services.send_services.email import (
    EmailNotificationService,
)
from apps.users.models.users import User
from apps.users.repositories.users import BaseUserRepository, ORMUserRepository
from apps.users.services.register import (
    BaseExistingUserValidatorService,
    BaseRegisterValidatorService,
    ComposedRegisterValidatorService,
    ExistingUserValidatorService,
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
    RegisterEmployeeUseCase,
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
    # apps/association_tables
    container.register(
        BaseUserGenreAssociationRepository,
        ORMUserGenreAssociationRepository,
        model_class=user_genre_association,
    )

    # apps/cinema
    container.register(BaseHallRepository, ORMHallRepository, model_class=Hall)
    container.register(BaseRowRepository, ORMRowRepository, model_class=Row)
    container.register(
        BasePlaceRepository, ORMPlaceRepository, model_class=Place
    )
    container.register(
        BaseFilmSessionRepository,
        ORMFilmSessionRepository,
        model_class=FilmSession,
    )

    # apps/films
    container.register(BaseFilmRepository, ORMFilmRepository, model_class=Film)
    container.register(
        BaseGenreRepository, ORMGenreRepository, model_class=Genre
    )
    container.register(
        BaseNotificationRepository,
        ORMNotificationRepository,
        model_class=Notification,
    )

    # apps/users
    container.register(BaseUserRepository, ORMUserRepository, model_class=User)


def _initialize_services(container: punq.Container) -> None:
    def build_user_validators() -> BaseRegisterValidatorService:
        return ComposedRegisterValidatorService(
            validators=[
                container.resolve(UniqueEmailValidatorService),
                container.resolve(PasswordIncorrectValidatorService),
            ],
        )

    def build_film_session_validators() -> BaseFilmSessionValidatorService:
        return ComposedFilmSessionValidator(
            validators=[
                container.resolve(FilmSessionValidatorService),
                container.resolve(FilmSessionIsDateTimeFreeValidatorService),
            ]
        )

    # apps/association_tables
    container.register(
        BaseUserGenreAssociationService, ORMUserGenreAssociationService
    )

    # apps/cinema
    container.register(BaseHallService, ORMHallService)
    container.register(
        BaseHallValidatorService, UniqueTitleHallValidatorService
    )
    container.register(BasePlaceService, ORMPlaceService)
    container.register(BasePlaceValidatorService, PlaceAlreadyExistsValidator)
    container.register(BaseRowService, ORMRowService)
    container.register(BaseRowValidatorService, RowAlreadyExistsValidator)

    # apps/films
    container.register(BaseFilmSessionService, ORMFilmSessionService)
    container.register(BaseFilmService, ORMFilmService)
    container.register(BaseFilmValidatorService, FilmRentDatesValidatorService)
    container.register(FilmSessionIsDateTimeFreeValidatorService)
    container.register(FilmSessionValidatorService)
    container.register(
        BaseFilmSessionValidatorService, factory=build_film_session_validators
    )
    container.register(BaseGenreService, ORMGenreService)

    # apps/users
    container.register(BaseUserService, ORMUserService)
    container.register(
        BaseRegisterValidatorService, factory=build_user_validators
    )
    container.register(UniqueEmailValidatorService)
    container.register(PasswordIncorrectValidatorService)
    container.register(
        BaseExistingUserValidatorService, ExistingUserValidatorService
    )
    container.register(BaseHallService, ORMHallService)


def _initialize_use_cases(container: punq.Container) -> None:
    # apps/cinema
    container.register(CreateHallUseCase)
    container.register(CreatePlaceUseCase)
    container.register(CreateRowUseCase)

    # apps/films
    container.register(CreateFilmUseCase)
    container.register(CreateFilmSessionUseCase)

    # apps/users
    container.register(RegisterUserUseCase)
    container.register(RegisterEmployeeUseCase)
    container.register(BaseRegisterUserUseCase, RegisterUserUseCase)
    container.register(BaseAuthUserUseCase, JwtBasedAuthUserUseCase)


def _initialize_external_staff(container: punq.Container) -> None:
    def _initialize_notification_service():
        return EmailNotificationService(
            logger=container.resolve(BaseLogger, module_name="notification")
        )

    container.register(BaseLogger, FileLogger)
    container.register(
        BaseNotificationService, factory=_initialize_notification_service
    )


def _initialize_container() -> punq.Container:
    container = punq.Container()

    _initialize_storage(container)
    _initialize_repositories(container)
    _initialize_services(container)
    _initialize_use_cases(container)
    _initialize_external_staff(container)

    return container
