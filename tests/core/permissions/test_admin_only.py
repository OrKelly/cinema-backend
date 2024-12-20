from core.permissions.base import AdminPermission
from tests.utils import create_test_app_with_route


class TestAdminOnlyPermission:
    async def test_get_admin_only_url_with_admin_user(self, admin_client, app):
        create_test_app_with_route(
            app=app,
            route_path="/test_auth",
            permission_classes=[AdminPermission],
        )
        response = await admin_client.get("/test_auth")
        assert response.status_code == 200

    async def test_get_admin_only_url_without_admin(self, logged_client, app):
        create_test_app_with_route(
            app=app,
            route_path="/test_auth",
            permission_classes=[AdminPermission],
        )
        response = await logged_client.get("/test_auth")
        assert response.status_code == 403
