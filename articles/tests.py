import json
from articles.models import Article
from backend.common.base_test import BaseTest, fake
from articles.api import router


class ArticlesTest(BaseTest):
    article_data = {
        "title": fake.sentence(),
        "slug": fake.slug(),
        "summary": fake.paragraph(),
        "tags": fake.sentence().split(),
        "meta_description": fake.sentence(),
        "content": "".join(fake.paragraphs()),
    }

    def get_router(self):
        return router

    def setUp(self) -> None:
        super().setUp()
        self.token = self._get_access_token()

    def _create_article(self):
        return self.client.post(
            "/",
            data=json.dumps(self.article_data),
            headers={"Authorization": f"Bearer {self.token}"},
        )

    def test_create_article(self):
        response = self._create_article()
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json()["title"], self.article_data["title"])

    def test_create_article_with_repeated_slug(self):
        response = self._create_article()
        self.assertEqual(response.status_code, 201)

        response = self._create_article()
        self.assertEqual(response.status_code, 409)

    def test_get_article(self):
        response = self._create_article()
        self.assertEqual(response.status_code, 201)

        response = self.client.get(f"/{self.article_data['slug']}")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["title"], self.article_data["title"])

    def test_get_non_existent_article(self):
        response = self.client.get("/nothing")
        self.assertEqual(response.status_code, 404)

    def test_update_article(self):
        response = self._create_article()
        self.assertEqual(response.status_code, 201)

        update_data = {"title": fake.sentence()}

        response = self.client.put(
            f"/{self.article_data['slug']}",
            data=json.dumps(update_data),
            headers={"Authorization": f"Bearer {self.token}"},
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["title"], update_data["title"])

    def test_delete_article(self):
        response = self._create_article()
        self.assertEqual(response.status_code, 201)

        response = self.client.delete(
            f"/{self.article_data['slug']}",
            headers={"Authorization": f"Bearer {self.token}"},
        )
        self.assertEqual(response.status_code, 204)

        with self.assertRaises(Article.DoesNotExist):
            Article.objects.get(slug=self.article_data["slug"])
