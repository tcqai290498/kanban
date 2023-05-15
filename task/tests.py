from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from .models import Process, Task


class TaskViewSetTestCase(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.process_data = {"title": "Test Process", "description": "This is a test process."}
        self.process = Process.objects.create(**self.process_data)
        self.task_data = {"process": self.process, "title": "Test Task", "description": "This is a test task."}
        self.task = Task.objects.create(**self.task_data)

    def test_create_task(self):
        new_task_data = {"process": self.process.id, "title": "New Task", "description": "This is a new task."}
        response = self.client.post("/task/", new_task_data, format="json")
        assert response.status_code == status.HTTP_201_CREATED
        self.assertEqual(Task.objects.count(), 2)

    def test_retrieve_task(self):
        response = self.client.get(f"/task/{self.task.id}/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["title"], self.task.title)

    def test_update_task(self):
        new_task_data = {"process": self.process.id, "title": "New Task", "description": "This is a new task."}
        response = self.client.put(f"/task/{self.task.id}/", new_task_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["title"], new_task_data["title"])

    def test_delete_task(self):
        response = self.client.delete(f"/task/{self.task.id}/")
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Task.objects.count(), 0)
