from django.urls import include, path
from rest_framework import routers

# from .views import (CategoryViewSet, CommentViewSet, GenreViewSet,
#                     RegistrationAPIView, ReviewViewSet, TitleViewSet,
#                     TokenObtain, UserViewSet)
from recipes.views import RecipeViewSet, TagViewSet, IngredientViewSet
from users.views import CustomUserViewSet

router_v1 = routers.DefaultRouter()
router_v1.register('users', CustomUserViewSet, basename='user')
router_v1.register('recipes', RecipeViewSet, basename='recipe')
router_v1.register('tags', TagViewSet, basename='tags')
router_v1.register('ingredients', IngredientViewSet, basename='ingredients')

urlpatterns = [
    path('', include(router_v1.urls)),
    # path('', include('djoser.urls')),
    path('auth/', include('djoser.urls.authtoken')),
]
