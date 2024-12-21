from functools import lru_cache

import punq

from apps.cinema.models.halls import Hall
from apps.cinema.repositories.halls import (
    BaseHallRepository,
    ORMHallRepository,
)
from apps.cinema.services.halls import (
    BaseHallService,
    BaseHallValidatorService,
    ORMHallService,
    UniqueTitleHallValidatorService,
)
from apps.cinema.use_cases.hall_create import CreateHallUseCase
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
from apps.films.models.films import Film
from apps.films.repositories.films import (
    BaseFilmRepository,
    BaseORMRepository,
)
from apps.films.services.films import (
    BaseFilmService, ORMFilmService
)
from apps.films.services.validation import (
    BaseValidationFilmService, FilmRentDatesValidatorService
)
from apps.films.use_cases.validation import (
    BaseValidationFilmUseCase, AddFilmUseCase
)


@lru_cache(1)
def get_container() -> punq.Container:
    return _initialize_container()


def _initialize_repositories(container: punq.Container) -> None:
    container.register(BaseUserRepository, ORMUserRepository, model_class=User)
    container.register(BaseHallRepository, ORMHallRepository, model_class=Hall)
    container.register(BaseFilmRepository, BaseORMRepository, model_class=Film)


def _initialize_services(container: punq.Container) -> None:
    def build_validators() -> BaseRegisterValidatorService:
        return ComposedRegisterValidatorService(
            validators=[
                container.resolve(UniqueEmailValidatorService),
                container.resolve(PasswordIncorrectValidatorService),
            ],
        )

    container.register(UniqueEmailValidatorService)
    container.register(PasswordIncorrectValidatorService)
    container.register(BaseUserService, ORMUserService)
    container.register(BaseRegisterValidatorService, factory=build_validators)
    container.register(
        BaseHallValidatorService, UniqueTitleHallValidatorService
    )
    container.register(BaseHallService, ORMHallService)
    container.register(BaseFilmService, ORMFilmService)
    container.register(
        BaseValidationFilmService, FilmRentDatesValidatorService
    )


def _initialize_use_cases(container: punq.Container) -> None:
    container.register(RegisterUserUseCase)
    container.register(CreateHallUseCase)
    container.register(BaseRegisterUserUseCase, RegisterUserUseCase)
    container.register(BaseAuthUserUseCase, JwtBasedAuthUserUseCase)
    container.register(BaseValidationFilmUseCase, AddFilmUseCase)


def _initialize_container() -> punq.Container:
    container = punq.Container()

    _initialize_repositories(container)
    _initialize_services(container)
    _initialize_use_cases(container)

    return container
