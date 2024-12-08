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
from apps.users.use_cases.register import RegisterUserUseCase
# from apps.cinema.models.halls import Hall
# from apps.cinema.repositories.halls import BaseHallsRepository, ORMHallRepository
from apps.cinema.models.rows import Row
from apps.cinema.repositories.rows import BaseRowRepository, ORMRowRepository
from apps.cinema.services.rows import BaseRowService, ORMRowService
from apps.users.use_cases.auth import (
    BaseAuthUserUseCase,
    JwtBasedAuthUserUseCase,
)
from apps.users.use_cases.register import (
    BaseRegisterUserUseCase,
    RegisterUserUseCase,
)


@lru_cache(1)
def get_container() -> punq.Container:
    return _initialize_container()


def _initialize_repositories(container: punq.Container) -> None:
    container.register(BaseUserRepository, ORMUserRepository, model_class=User)
    container.register(BaseHallRepository, ORMHallRepository, model_class=Hall)

    container.register(BaseRowRepository, ORMRowRepository, model_class=Row)

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
    container.register(BaseRowService, ORMRowService)
    container.register(BaseRegisterValidatorService, factory=build_validators)
    container.register(
        BaseHallValidatorService, UniqueTitleHallValidatorService
    )
    container.register(BaseHallService, ORMHallService)


def _initialize_use_cases(container: punq.Container) -> None:
    container.register(RegisterUserUseCase)
    container.register(CreateHallUseCase)
    container.register(BaseRegisterUserUseCase, RegisterUserUseCase)
    container.register(BaseAuthUserUseCase, JwtBasedAuthUserUseCase)


def _initialize_container() -> punq.Container:
    container = punq.Container()

    _initialize_repositories(container)
    _initialize_services(container)
    _initialize_use_cases(container)

    return container
