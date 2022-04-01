from django.contrib.auth import get_user_model
from djoser.views import UserViewSet
from rest_framework import permissions, status
from rest_framework.decorators import action
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response

from recipes.serializers import SubscribeSerializer
from users.models import Subscribe
from users.serializers import UserSerializer

User = get_user_model()


class CustomUserViewSet(UserViewSet):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = UserSerializer

    @action(methods=['POST', 'DELETE'], detail=True)
    def subscribe(self, request, id):
        user = request.user
        author = get_object_or_404(User, pk=id)
        if request.method == 'DELETE':
            if not Subscribe.objects.filter(user=user, author=author).exists():
                return Response(
                    data={'errors': f'Вы не подписаны на автора {author}'},
                    status=status.HTTP_400_BAD_REQUEST
                )
            Subscribe.objects.get(user=user, author=author).delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        if user == author:
            return Response(
                data={'errors': 'Нельзя подписаться на самого себя'},
                status=status.HTTP_400_BAD_REQUEST
            )
        if Subscribe.objects.filter(user=user, author=author).exists():
            return Response(
                data={'errors': f'Вы уже подписаны на автора {author}'},
                status=status.HTTP_400_BAD_REQUEST
            )
        Subscribe.objects.create(user=user, author=author)
        serializer = SubscribeSerializer(
            instance=author,
            context={'request': request},
        )
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @action(methods=['GET'], detail=False)
    def subscriptions(self, request):
        queryset = User.objects.filter(subscribing__user=request.user)
        page = self.paginate_queryset(queryset)
        serializer = SubscribeSerializer(instance=page, many=True,
                                         context={'request': request})
        return self.get_paginated_response(serializer.data)
