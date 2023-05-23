from rest_framework import viewsets, status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from process.models import Process
from task.models import Task
from task.serializers import TaskSerializer


# Create your views here.
class TaskViewSet(viewsets.ModelViewSet):
    permission_classes = [AllowAny]
    serializer_class = TaskSerializer
    queryset = Task.objects.all()

    def create(self, request, *args, **kwargs):
        process_id = request.data.get("process", None)
        if process_id is None:
            return Response({"error": "process field is required"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            process = Process.objects.get(id=process_id)
        except Process.DoesNotExist:
            return Response({"error": f"process with id {process_id} does not exist"}, status=status.HTTP_404_NOT_FOUND)

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        serializer.save(process=process)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
