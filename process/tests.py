from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from process.models import Process


class ProcessViewSetTestCase(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.process_data = {"title": "Test Process", "description": "This is a test process."}
        self.process = Process.objects.create(**self.process_data)

    def test_create_process(self):
        response = self.client.post("/process/", self.process_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Process.objects.count(), 2)

    def test_retrieve_process(self):
        response = self.client.get(f"/process/{self.process.id}/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["title"], self.process.title)

    def test_update_process(self):
        new_process_data = {"title": "New Process", "description": "This is a new process."}
        response = self.client.put(f"/process/{self.process.id}/", new_process_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["title"], new_process_data["title"])

    def test_delete_process(self):
        response = self.client.delete(f"/process/{self.process.id}/")
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Process.objects.count(), 0)
