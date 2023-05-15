from django.db import models

from process.models import Process


# Create your models here.
class Task(models.Model):
    process = models.ForeignKey(Process, on_delete=models.CASCADE, related_name="subtasks")
    title = models.CharField(max_length=255)
    description = models.TextField()
