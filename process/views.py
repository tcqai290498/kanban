from rest_framework import viewsets
from rest_framework.permissions import AllowAny

from .models import Process
from .serializers import ProcessSerializer


class ProcessViewSet(viewsets.ModelViewSet):
    permission_classes = [AllowAny]
    queryset = Process.objects.all()
    serializer_class = ProcessSerializer
