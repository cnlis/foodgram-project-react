from django.urls import include, path
from rest_framework import routers

# from .views import (CategoryViewSet, CommentViewSet, GenreViewSet,
#                     RegistrationAPIView, ReviewViewSet, TitleViewSet,
#                     TokenObtain, UserViewSet)

router_v1 = routers.DefaultRouter()
# router_v1.register('categories', CategoryViewSet)
# router_v1.register('genres', GenreViewSet)
# router_v1.register('titles', TitleViewSet)
# router_v1.register(
#     r'titles/(?P<title_id>\d+)/reviews',
#     ReviewViewSet,
#     basename='review'
# )
# router_v1.register(
#     r'titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/comments',
#     CommentViewSet,
#     basename='comment'
# )
# router_v1.register('users', UserViewSet, basename='user')

urlpatterns = [
    path('', include(router_v1.urls)),
    path('', include('djoser.urls')),
    path('auth/', include('djoser.urls.authtoken')),
]