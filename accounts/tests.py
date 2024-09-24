import json
from django.test import TestCase
from ninja.testing import TestClient
from accounts.api import router


class UserAuthTest(TestCase):
    def setUp(self) -> None:
        self.client = TestClient(router)
        self.user_data = {
            "username": "testuser",
            "email": "testuser@testing.com",
            "password": "JMdbdV2f",
        }

        self.login_data = {
            "username": "testuser",
            "password": "JMdbdV2f",
        }

    def _register_user(self):
        response = self.client.post(
            "/users",
            data=json.dumps(self.user_data),
        )
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json()["username"], self.user_data["username"])

        return response

    def _login_user(self):
        response = self.client.post(
            "/users/login",
            data=json.dumps(self.login_data),
        )
        self.assertEqual(response.status_code, 200)
        self.assertIn("token", response.json())

        return response.json()["token"]

    def test_user_registration(self):
        self._register_user()

    def test_user_registration_already_exists(self):
        self._register_user()

        response = self.client.post(
            "/users",
            data=json.dumps(self.user_data),
        )
        self.assertEqual(response.status_code, 409)

    def test_user_login(self):
        self._register_user()
        self._login_user()

    def test_user_login_with_incorrect_credentials(self):
        self._register_user()

        login_data = {
            "username": "testuser",
            "password": "wrongpassword",
        }
        response = self.client.post(
            "/users/login",
            data=json.dumps(login_data),
        )
        self.assertEqual(response.status_code, 401)

    def test_get_current_user(self):
        self._register_user()
        token = self._login_user()

        response = self.client.get(
            "/user",
            headers={"Authorization": f"Bearer {token}"},
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["username"], self.user_data["username"])

    def test_get_current_user_while_unauthenticated(self):
        response = self.client.get("/user")
        self.assertEqual(response.status_code, 401)
        self.assertEqual(response.json(), {"detail": "Unauthorized"})

    def test_update_user(self):
        self._register_user()
        token = self._login_user()

        update_data = {"email": "updateduser@testing.com"}

        response = self.client.put(
            "/user",
            data=json.dumps(update_data),
            headers={"Authorization": f"Bearer {token}"},
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["email"], update_data["email"])

    def test_update_user_without_body(self):
        self._register_user()
        token = self._login_user()

        response = self.client.put(
            "/user",
            headers={"Authorization": f"Bearer {token}"},
        )
        self.assertEqual(response.status_code, 422)
