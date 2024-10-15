from django.contrib.auth.models import User
from backend.common.base_test import BaseTest
from social.models import Follow
from social.api import router


class SocialTest(BaseTest):
    follows = [
        {
            "username": "follower1",
            "email": "follower1@gmail.com",
        },
        {
            "username": "follower2",
            "email": "follower2@gmail.com",
        },
    ]

    def get_router(self):
        return router

    def setUp(self) -> None:
        super().setUp()
        self.create_followers()

    def create_followers(self):
        for follower in self.follows:
            User.objects.create_user(
                follower["username"],
                follower["email"],
                self.password,
            )

    def test_user_can_not_follow_itself(self) -> None:
        token = self._get_access_token()
        response = self.client.post(
            f"/{self.username}/follow",
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

        following_count = Follow.objects.filter(follower=self.user).count()
        self.assertEqual(following_count, 1)

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

        following_count = Follow.objects.filter(follower=self.user).count()
        self.assertEqual(following_count, 0)

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
            f"/{self.username}/following",
            headers={"Authorization": f"Bearer {token}"},
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()), len(self.follows))
