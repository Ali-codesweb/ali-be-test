from django.test import TestCase
from rest_framework.test import APIClient


class TestTestView(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_test_view(self):
        response = self.client.get("/api/openapi/test")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, "hello ok")
