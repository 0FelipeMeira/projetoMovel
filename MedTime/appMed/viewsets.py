from rest_framework import viewsets
from .models import Registro, RegistroMed
from .serializers import RegistroSerializer, RegistroMedSerializer

class RegistroViewSet(viewsets.ModelViewSet):
    queryset = Registro.objects.all()
    serializer_class = RegistroSerializer

class RegistroMedViewSet(viewsets.ModelViewSet):
    queryset = RegistroMed.objects.all()
    serializer_class = RegistroMedSerializer

