from rest_framework.viewsets import ModelViewSet
from .serializers import (
    Usuario,
    UsuarioSerializer,
)


class UsuarioViewSet(ModelViewSet):
    queryset = Usuario.objects.all()
    serializer_class = UsuarioSerializer
