from django.contrib.auth.models import User
from django.test import TestCase
from ninja.testing import TestClient
from ninja_jwt.tokens import RefreshToken
from faker import Faker

fake = Faker()
fake_profile = fake.simple_profile()


class BaseTest(TestCase):
    username = fake_profile.get("username")
    email = fake_profile.get("email")
    password = fake.password()
    public_name = fake_profile.get("name")
    biography = fake.sentence()
    birthday = fake_profile.get("birthday")

    def setUp(self) -> None:
        self.client = TestClient(self.get_router())
        self.user = self.create_user()

    def create_user(self) -> User:
        return User.objects.create_user(
            self.username,
            self.email,
            self.password,
        )

    def _get_access_token(self) -> str:
        refresh = RefreshToken.for_user(self.user)
        return f"{refresh.access_token}"

    def get_router(self):
        raise NotImplementedError("Subclasses must implement get_router method")
