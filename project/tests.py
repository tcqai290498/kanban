from django.contrib.auth.models import User
from rest_framework.test import APITestCase
from rest_framework.authtoken.models import Token


class AuthenticationTestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(email="admin@admin.com", password="admin")

    def test_login(self):
        url = "/api/login/"
        data = {"email": "admin@admin.com", "password": "admin"}

        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 200)
        self.assertTrue("token" in response.data)

    def test_logout(self):
        url = "/api/logout/"
        self.client.force_authenticate(user=self.user)

        # Retrieve the authentication token
        token = Token.objects.get(user=self.user)
        headers = {"Authorization": "Token " + token.key}

        response = self.client.post(url, headers=headers)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["detail"], "Logout successful")
