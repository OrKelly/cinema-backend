from httpx import AsyncClient

from apps.users.exceptions.auth import NoDataInFieldException
from apps.users.services.users import BaseUserService
from core.containers import get_container
from core.enums import RoleKindEnum
from tests.factories.user import UserFactory

user_service = get_container().resolve(BaseUserService)


class TestEmployeeApi:
    @staticmethod
    def get_list_url(*args, **kwargs):
        return "/".join(("api/v1/employees", *map(str, args)))

    async def test_employee_register_from_user(
        self, prepare_database, admin_client: AsyncClient
    ):
        user = await UserFactory().create()
        employees_before_request = await user_service.get_by_filter(
            filter_params={"role": RoleKindEnum.EMPLOYEE}
        )
        users_before_request = await user_service.get_by_filter(
            filter_params={"role": RoleKindEnum.CLIENT}
        )
        response = await admin_client.post(
            self.get_list_url(), json={"user_id": user.id}
        )
        employees_after_request = await user_service.get_by_filter(
            filter_params={"role": RoleKindEnum.EMPLOYEE}
        )
        users_after_request = await user_service.get_by_filter(
            filter_params={"role": RoleKindEnum.CLIENT}
        )
        response_json = response.json()["data"]
        assert response.status_code == 200
        assert response_json["status"] == "Сотрудник успешно зарегистрирован"
        assert len(employees_before_request) == 0
        assert len(employees_after_request) == 1
        assert len(users_before_request) == 1
        assert len(users_after_request) == 0

    async def test_employee_register_from_new_user(
        self, prepare_database, admin_client: AsyncClient
    ):
        employees_before_request = await user_service.get_by_filter(
            filter_params={"role": RoleKindEnum.EMPLOYEE}
        )
        user_data = await UserFactory().row()
        user_data.pop("password")
        payload = {"employee_data": user_data}
        response = await admin_client.post(self.get_list_url(), json=payload)
        employees_after_request = await user_service.get_by_filter(
            filter_params={"role": RoleKindEnum.EMPLOYEE}
        )
        response_json = response.json()["data"]
        assert response.status_code == 200
        assert response_json["status"] == "Сотрудник успешно зарегистрирован"
        assert len(employees_before_request) == 0
        assert len(employees_after_request) == 1

    async def test_employee_register_without_data(
        self, admin_client: AsyncClient
    ):
        response = await admin_client.post(self.get_list_url(), json={})
        response_json = response.json()
        assert response.status_code == 422
        assert response_json["message"] == NoDataInFieldException().message

    async def test_employee_register_without_admin_permission(
        self, logged_client: AsyncClient
    ):
        user = await UserFactory().create()
        payload = {"user_id": user.id}
        response = await logged_client.post(self.get_list_url(), json=payload)
        assert response.status_code == 403
        assert response.json()["detail"] == "Доступ запрещен"
