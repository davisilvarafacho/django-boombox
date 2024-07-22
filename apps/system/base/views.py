from django.db.models import ProtectedError

from rest_framework import status
from rest_framework.decorators import action
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response


class BaseViewSet(ModelViewSet):
    serializer_classes = {}
    filterset_fields = {}
    search_fields = []

    def get_serializer_class(self):
        assert self.serializer_classes != {} or self.serializer_class is not None, (
            "'%s' deve implementar o 'serializer_class' ou  'serializer_classes'." % self.__class__.__name__
        )

        if self.serializer_class:
            return self.serializer_class
        
        if action is None:
            action = self.action

        return self.serializer_classes[action]

    def destroy(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            self.perform_destroy(instance)
            return Response(status=status.HTTP_204_NO_CONTENT)

        except ProtectedError as ex:
            return Response({'error': ex.args[0]}, status=status.HTTP_409_CONFLICT)

    @action(methods=["get"], detail=True)
    def clonar(self, request):
        instance = self.get_object()
        instance.pk = None
        instance.save()
        serializer = self.get_serializer(instance)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @action(methods=["post"], detail=False)
    def bulk_create(self, request):
        serializer = self.get_serializer(data=request.data, many=True)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
