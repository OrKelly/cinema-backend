from core.permissions.base import ClientPermission
from tests.utils import create_test_app_with_route


class TestClientOnlyPermission:
    async def test_get_client_only_url_with_logged_client(
        self, logged_client, app
    ):
        create_test_app_with_route(
            app=app,
            route_path="/test_auth",
            permission_classes=[ClientPermission],
        )
        response = await logged_client.get("/test_auth")
        assert response.status_code == 200

    async def test_get_client_only_url_without_client(
        self, employee_client, app
    ):
        create_test_app_with_route(
            app=app,
            route_path="/test_auth",
            permission_classes=[ClientPermission],
        )
        response = await employee_client.get("/test_auth")
        assert response.status_code == 403
