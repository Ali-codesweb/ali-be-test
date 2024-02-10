from django.test import TestCase
from rest_framework.test import APIClient


class TestTestView(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_test_view(self):
        response = self.client.get("/api/openapi/test")
        self.assertEqual(response.status_code, 200)

    def test_generate_ad_prompt_view(self):
        response = self.client.post("/api/openapi/", {
            "product_description": "Some random product",
            "vibe_words": "cool, simple,elegant"
        })
        self.assertEqual(response.status_code, 200)
