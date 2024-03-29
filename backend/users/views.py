from django.contrib.auth import get_user_model
from django.db.models import Count, Exists
from django.utils.translation import gettext_lazy as _
from djoser.views import UserViewSet
from rest_framework import permissions, status
from rest_framework.decorators import action
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response

from recipes.mixins import ResponseMixin
from recipes.serializers import SubscribeSerializer
from users.models import Subscribe

User = get_user_model()


class CustomUserViewSet(ResponseMixin, UserViewSet):
    """Подписки на авторов и список подписок."""

    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return User.objects.annotate(
            is_subscribed=Exists(
                User.objects.filter(subscribing__user=self.request.user)),
            recipes_count=Count('recipe')
        ).prefetch_related('recipe')

    @action(methods=['POST', 'DELETE'], detail=True)
    def subscribe(self, request, id):
        user = request.user
        author = get_object_or_404(User, pk=id)
        if request.method == 'DELETE':
            deleted, lst = user.subscriber.filter(author=author).delete()
            return self.delete_response(deleted, author)
        if user == author:
            return Response(
                data={'errors': _('Нельзя подписаться на самого себя')},
                status=status.HTTP_400_BAD_REQUEST
            )
        obj, created = Subscribe.objects.get_or_create(
            user=user, author=author)
        author = get_object_or_404(self.get_queryset(), pk=id)
        return self.create_response(created, author, SubscribeSerializer)

    @action(methods=['GET'], detail=False)
    def subscriptions(self, request):
        queryset = self.get_queryset().filter(subscribing__user=request.user)
        page = self.paginate_queryset(queryset)
        serializer = SubscribeSerializer(instance=page, many=True,
                                         context={'request': request})
        return self.get_paginated_response(serializer.data)
