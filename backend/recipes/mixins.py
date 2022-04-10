from django.utils.translation import gettext_lazy as _
from rest_framework import status
from rest_framework.response import Response


class ResponseMixin:
    """Ответы сервера на добавление и удаление объектов."""

    def create_response(self, created, obj, serializer_class):
        if created:
            serializer = serializer_class(
                instance=obj, context={'request': self.request}, )
            return Response(data=serializer.data,
                            status=status.HTTP_201_CREATED)
        return Response(
            data={'errors': (_('Объект {} уже добавлен').format(obj))},
            status=status.HTTP_400_BAD_REQUEST
        )

    def delete_response(self, deleted, obj):
        if deleted:
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response(
            data={'errors': (_('Объект {} отсутствует').format(obj))},
            status=status.HTTP_400_BAD_REQUEST
        )
