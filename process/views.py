from rest_framework import viewsets
from rest_framework.permissions import AllowAny

from process.models import Process
from process.serializers import ProcessSerializer


class ProcessViewSet(viewsets.ModelViewSet):
    permission_classes = [AllowAny]
    queryset = Process.objects.all()
    serializer_class = ProcessSerializer
