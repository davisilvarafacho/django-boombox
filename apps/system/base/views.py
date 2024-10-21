from django.db.models import ProtectedError

from rest_framework import status
from rest_framework.decorators import action
from rest_framework.exceptions import ValidationError
from rest_framework.viewsets import ModelViewSet, GenericViewSet
from rest_framework.response import Response


class BaseViewSet(GenericViewSet):
    serializer_classes = {}
    serializer_class = None
    filterset_fields = {}
    search_fields = []

    def get_queryset(self):
        queryset = super().get_queryset()

        distinct_fields = self.request.query_params.get("distinct", None)
        if distinct_fields is not None:
            queryset = queryset.distinct(*distinct_fields)

        return queryset

    def get_serializer_class(self):
        assert self.serializer_classes != {} or self.serializer_class is not None, (
            "'%s' deve implementar o 'serializer_class' ou  'serializer_classes'."
            % self.__class__.__name__
        )

        if self.serializer_class:
            return self.serializer_class

        return self.serializer_classes[self.action]


class BaseModelViewSet(ModelViewSet):
    serializer_classes = {}
    serializer_class = None
    filterset_fields = {}
    search_fields = []
    ordering_fields = []

    def get_object(self):
        instance = super().get_object()
        self.instance = instance
        return instance

    def get_aditional_serializer_context(self):
        return {}

    def get_serializer_context(self):
        context = super().get_serializer_context()
        aditional_context = self.get_aditional_serializer_context()
        return {"action": self.action, **context, **aditional_context}

    def perform_create(self, serializer, **overwrite):
        serializer.save(owner=self.request.user, **overwrite)

    def destroy(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            self.perform_destroy(instance)
            return Response(status=status.HTTP_204_NO_CONTENT)

        except ProtectedError:
            return Response(
                {"mensagem": "Esse registro não pode ser excluído por estar vínculado a outro registro na base de dados"},
                status=status.HTTP_409_CONFLICT,
            )

    @action(methods=["post"], detail=False)
    def bulk_create(self, request):
        serializer = self.get_serializer(data=request.data, many=True)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(
            serializer.data, status=status.HTTP_201_CREATED, headers=headers
        )

    @action(methods=["get"], detail=True)
    def clonar(self, request, pk):
        instance = self.get_object()
        instance.pk = None
        self.alterar_campos_unicos(instance)
        instance.save()
        serializer = self.get_serializer(instance)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def alterar_campos_unicos(self, instance):
        """Método para alterar campos com `unique=True` na action `clonar
        """
        pass
