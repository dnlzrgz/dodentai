from datetime import datetime, timezone
from django.contrib.auth.models import User
from django.test import TestCase
from ninja.testing import TestClient
from ninja_jwt.tokens import RefreshToken
from social.api import router


class SocialTest(TestCase):
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
            "username": "testuser",
            "password": "JMdbdV2f",
        }

        self.user = User.objects.create_user(
            self.user_data["username"],
            self.user_data["email"],
            self.user_data["password"],
        )

        self.follows = [
            {
                "username": "follower1",
                "email": "follower1@gmail.com",
            },
            {
                "username": "follower2",
                "email": "follower2@gmail.com",
            },
        ]

        for follower in self.follows:
            User.objects.create_user(
                follower["username"],
                follower["email"],
                self.user_data["password"],
            )

    def _get_access_token(self) -> str:
        refresh = RefreshToken.for_user(self.user)
        return f"{refresh.access_token}"

    def test_user_can_not_follow_itself(self) -> None:
        token = self._get_access_token()
        response = self.client.post(
            f"/{self.user_data['username']}/follow",
            headers={"Authorization": f"Bearer {token}"},
        )
        self.assertEqual(response.status_code, 403)

    def test_user_can_follow_other_users(self) -> None:
        token = self._get_access_token()
        follow_username = self.follows[0]["username"]

        # Make follow request
        response = self.client.post(
            f"/{follow_username}/follow",
            headers={"Authorization": f"Bearer {token}"},
        )
        self.assertEqual(response.status_code, 200)

        # Check following count
        response = self.client.get(
            f"/{self.user_data['username']}/following/count",
            headers={"Authorization": f"Bearer {token}"},
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["count"], 1)

    def test_user_can_unfollow_users(self) -> None:
        token = self._get_access_token()
        follow_username = self.follows[0]["username"]

        # Make follow request
        response = self.client.post(
            f"/{follow_username}/follow",
            headers={"Authorization": f"Bearer {token}"},
        )
        self.assertEqual(response.status_code, 200)

        # Make unfollow request
        response = self.client.post(
            f"/{follow_username}/follow",
            headers={"Authorization": f"Bearer {token}"},
        )
        self.assertEqual(response.status_code, 200)

        # Check following count
        response = self.client.get(
            f"/{self.user_data['username']}/following/count",
            headers={"Authorization": f"Bearer {token}"},
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["count"], 0)

    def test_get_following_list(self) -> None:
        token = self._get_access_token()

        # Make follow requests
        for follow in self.follows:
            response = self.client.post(
                f"/{follow['username']}/follow",
                headers={"Authorization": f"Bearer {token}"},
            )
            self.assertEqual(response.status_code, 200)

        # Get following users
        response = self.client.get(
            f"/{self.user_data['username']}/following",
            headers={"Authorization": f"Bearer {token}"},
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()), len(self.follows))
