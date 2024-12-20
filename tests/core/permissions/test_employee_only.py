from core.permissions.base import EmployeePermission
from tests.utils import create_test_app_with_route


class TestEmployeeOnlyPermission:
    async def test_get_employee_only_url_with_employee_user(
        self, employee_client, app
    ):
        create_test_app_with_route(
            app=app,
            route_path="/test_auth",
            permission_classes=[EmployeePermission],
        )
        response = await employee_client.get("/test_auth")
        assert response.status_code == 200

    async def test_get_employee_only_url_without_employee(
        self, logged_client, app
    ):
        create_test_app_with_route(
            app=app,
            route_path="/test_auth",
            permission_classes=[EmployeePermission],
        )
        response = await logged_client.get("/test_auth")
        assert response.status_code == 403
