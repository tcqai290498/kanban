from rest_framework import serializers
from task.serializers import TaskSerializer
from .models import Process


class ProcessSerializer(serializers.ModelSerializer):
    tasks = serializers.SerializerMethodField()

    class Meta:
        model = Process
        fields = ["id", "title", "description", "tasks"]

    def get_tasks(self, instance):
        tasks = instance.subtasks.all()
        task_serializer = TaskSerializer(tasks, many=True)
        return task_serializer.data

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation["tasks"] = self.get_tasks(instance)
        return representation
