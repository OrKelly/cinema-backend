from abc import ABC, abstractmethod
from dataclasses import dataclass

from apps.users.models.users import User
from core.enums import RoleKindEnum


@dataclass
class BasePermission(ABC):
    user: User

    @abstractmethod
    async def check_permission(self, *args, **kwargs) -> bool: ...


@dataclass
class AuthenticatedPermission(BasePermission):
    async def check_permission(self, *args, **kwargs) -> bool:
        return True if self.user else False


@dataclass
class AdminPermission(BasePermission):
    async def check_permission(self, *args, **kwargs) -> bool:
        if self.user:
            return self.user.role == RoleKindEnum.ADMIN
        return None


@dataclass
class EmployeePermission(BasePermission):
    async def check_permission(self, *args, **kwargs) -> bool:
        if self.user:
            return self.user.role == RoleKindEnum.EMPLOYEE
        return None


@dataclass
class ClientPermission(BasePermission):
    async def check_permission(self, *args, **kwargs) -> bool:
        if self.user:
            return self.user.role == RoleKindEnum.CLIENT
        return None
