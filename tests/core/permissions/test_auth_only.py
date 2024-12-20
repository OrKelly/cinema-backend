from core.permissions.base import AuthenticatedPermission
from tests.utils import create_test_app_with_route


class TestAuthOnlyPermission:
    async def test_get_auth_only_url_with_logged_user(
        self, logged_client, app
    ):
        create_test_app_with_route(
            app=app,
            route_path="/test_auth",
            permission_classes=[AuthenticatedPermission],
        )
        response = await logged_client.get("/test_auth")
        assert response.status_code == 200

    async def test_get_auth_only_url_without_auth(self, client, app):
        create_test_app_with_route(
            app=app,
            route_path="/test_auth",
            permission_classes=[AuthenticatedPermission],
        )
        response = await client.get("/test_auth")
        assert response.status_code == 403
