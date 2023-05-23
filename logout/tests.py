from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token


class LogoutAPIViewTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.logout_url = reverse("logout")
        self.user = User.objects.create_user(email="testuser@example.com", username="testuser", password="testpassword")
        self.token = Token.objects.create(user=self.user)

    def test_logout_success(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.post(self.logout_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, {"detail": "Logout successful"})
        # Verify that the token has been deleted
        self.assertFalse(Token.objects.filter(user=self.user).exists())

    def test_logout_unauthenticated(self):
        response = self.client.post(self.logout_url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        # Verify that the token has not been deleted
        self.assertTrue(Token.objects.filter(user=self.user).exists())
