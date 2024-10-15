import json
from backend.common.base_test import BaseTest
from profiles.models import Profile
from profiles.api import router


class ProfilesTest(BaseTest):
    def get_router(self):
        return router

    def test_profile_exists_for_new_user(self):
        profile = Profile.objects.get(user=self.user)
        self.assertIsNotNone(profile)

    def test_get_user_profile(self):
        response = self.client.get(f"/{self.username}")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["username"], self.username)

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
