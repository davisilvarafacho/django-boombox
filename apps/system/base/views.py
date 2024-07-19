from django.db.models import ProtectedError

from rest_framework import status
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response


class BaseViewSet(ModelViewSet):
    serializer_classes = {}
    filterset_fields = {}
    search_fields = []

    def initial(self, request, *args, **kwargs):
        super().initial(request, *args, **kwargs)
        self.token = request.headers.get("Authorization").split(" ")[1]
    
    def get_serializer_class(self):
        assert self.serializer_classes != {} and self.serializer_class is not None, (
            "'%s' should either include a `serializer_class` attribute, "
            "or, fill the `serializer_classes` attribute with serializers "
            "for the default actions or override the `get_serializer_class()` "
            "method." % self.__class__.__name__
        )

        if self.serializer_class:
            return self.serializer_class

        return self.serializer_classes[self.action]

    def destroy(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            self.perform_destroy(instance)
            return Response(status=status.HTTP_204_NO_CONTENT)

        except ProtectedError as ex:
            return Response({'error': ex.args[0]}, status=status.HTTP_409_CONFLICT)

