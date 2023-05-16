from django.contrib.auth.models import User
from rest_framework.test import APITestCase
from rest_framework.authtoken.models import Token


class AuthenticationTestCase(APITestCase):
    token = ""

    def setUp(self):
        self.user = User.objects.create_user(username="admin", email="admin@admin.com", password="admin")

    def test_login(self):
        url = "/login/"
        data = {"email": "admin@admin.com", "password": "admin"}

        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 200)
        self.assertTrue("token" in response.data)
        self.token = response.data["token"]

    def test_logout(self):
        url = "/logout/"
        self.client.force_authenticate(user=self.user)

        # Retrieve the authentication token
        token, _ = Token.objects.get_or_create(user=self.user)
        headers = {"Authorization": "Token " + token.key}

        response = self.client.post(url, headers=headers)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["detail"], "Logout successful")
