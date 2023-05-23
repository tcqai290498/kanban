from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from django.contrib.auth.models import User


class LoginAPIViewTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.login_url = reverse("login")
        self.user = User.objects.create_user(username="admin", email="admin@admin.com", password="admin")

    def test_login_success(self):
        data = {"email": "admin@admin.com", "password": "admin"}
        response = self.client.post(self.login_url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("token", response.data)

    def test_login_invalid_credentials(self):
        data = {"email": "testuser@example.com", "password": "wrongpassword"}
        response = self.client.post(self.login_url, data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(response.data["detail"], "Invalid credentials")
