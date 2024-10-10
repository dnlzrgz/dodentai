import json
from datetime import datetime, timezone
from django.contrib.auth.models import User
from django.test import TestCase
from ninja.testing import TestClient
from ninja_jwt.tokens import RefreshToken
from profiles.models import Profile
from profiles.api import router


class ProfileTest(TestCase):
    def setUp(self) -> None:
        self.client = TestClient(router)

        self.user_data = {
            "username": "testuser",
            "email": "testuser@testing.com",
            "password": "JMdbdV2f",
            "public_name": "tester",
            "biography": "Python developer",
            "birthday": datetime.now(timezone.utc),
        }

        self.login_data = {
            "username": self.user_data["username"],
            "password": self.user_data["password"],
        }

        self.user = User.objects.create_user(
            self.user_data["username"],
            self.user_data["email"],
            self.user_data["password"],
        )

    def _get_access_token(self) -> str:
        refresh = RefreshToken.for_user(self.user)
        return f"{refresh.access_token}"

    def test_profile_exists_for_new_user(self):
        profile = Profile.objects.get(user=self.user)
        self.assertIsNotNone(profile)

    def test_get_user_profile(self):
        response = self.client.get(f"/{self.user_data['username']}")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["username"], self.user_data["username"])

    def test_get_non_existant_user_profile(self):
        response = self.client.get("/none")
        self.assertEqual(response.status_code, 404)

    def test_update_user_profile(self):
        token = self._get_access_token()

        update_data = {"biography": "Django developer."}

        response = self.client.put(
            "/",
            data=json.dumps(update_data),
            headers={"Authorization": f"Bearer {token}"},
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["biography"], update_data["biography"])
