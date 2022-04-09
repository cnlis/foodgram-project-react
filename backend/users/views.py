from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _
from djoser.views import UserViewSet
from rest_framework import permissions, status
from rest_framework.decorators import action
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response

from recipes.serializers import SubscribeSerializer
from users.models import Subscribe

User = get_user_model()


class CustomUserViewSet(UserViewSet):
    """Подписки на авторов и список подписок."""

    permission_classes = [permissions.IsAuthenticated]

    @action(methods=['POST', 'DELETE'], detail=True)
    def subscribe(self, request, id):
        user = request.user
        author = get_object_or_404(User, pk=id)
        if request.method == 'DELETE':
            deleted, lst = Subscribe.objects.filter(
                user=user, author=author).delete()
            if deleted:
                return Response(status=status.HTTP_204_NO_CONTENT)
            return Response(
                data={'errors': _('Вы не подписаны на '
                                  'автора {}').format(author)},
                status=status.HTTP_400_BAD_REQUEST
            )

        if user == author:
            return Response(
                data={'errors': _('Нельзя подписаться на самого себя')},
                status=status.HTTP_400_BAD_REQUEST
            )
        obj, created = Subscribe.objects.get_or_create(
            user=user, author=author)
        if created:
            serializer = SubscribeSerializer(
                instance=author,
                context={'request': request},
            )
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(
            data={'errors': _('Вы уже подписаны на '
                              'автора {}').format(author)},
            status=status.HTTP_400_BAD_REQUEST
        )

    @action(methods=['GET'], detail=False)
    def subscriptions(self, request):
        queryset = User.objects.filter(subscribing__user=request.user)
        page = self.paginate_queryset(queryset)
        serializer = SubscribeSerializer(instance=page, many=True,
                                         context={'request': request})
        return self.get_paginated_response(serializer.data)
