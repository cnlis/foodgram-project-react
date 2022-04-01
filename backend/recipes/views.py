from django.db.models import Sum
from django.http import HttpResponse
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, permissions, status, viewsets, mixins
from rest_framework.decorators import action
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response

from .filters import RecipeFilter
from .models import Favorite, Ingredient, Recipe, ShoppingCart, Tag
from .permissions import IsAuthorOrReadOnly
from .serializers import RecipeSerializer, TagSerializer, IngredientSerializer

from .utilities import generate_pdf


class ReadOnlyViewSet(mixins.RetrieveModelMixin, mixins.ListModelMixin,
                      viewsets.GenericViewSet):
    pass


class TagViewSet(ReadOnlyViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer


class IngredientViewSet(ReadOnlyViewSet):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)


class RecipeViewSet(viewsets.ModelViewSet):
    queryset = Recipe.objects.all()
    permission_classes = (IsAuthorOrReadOnly,)
    serializer_class = RecipeSerializer
    filter_backends = (DjangoFilterBackend,)
    filterset_class = RecipeFilter

    def add_delete_item(self, request, pk, model, dest_str):
        user = request.user
        recipe = get_object_or_404(Recipe, pk=pk)
        if request.method == 'DELETE':
            if not model.objects.filter(user=user, recipe=recipe).exists():
                return Response(
                    data={'errors': f'Нет рецепта "{recipe}" в {dest_str}'},
                    status=status.HTTP_400_BAD_REQUEST
                )
            model.objects.get(user=user, recipe=recipe).delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        if model.objects.filter(user=user, recipe=recipe).exists():
            return Response(
                data={'errors': f'Рецепт {recipe} уже в {dest_str}'},
                status=status.HTTP_400_BAD_REQUEST
            )
        model.objects.create(user=user, recipe=recipe)
        serializer = self.get_serializer(
            instance=recipe, context={'request': request},)
        return Response(data=serializer.data, status=status.HTTP_201_CREATED)

    @action(methods=['POST', 'DELETE'], detail=True,
            permission_classes=[permissions.IsAuthenticated])
    def favorite(self, request, pk):
        return self.add_delete_item(request, pk, Favorite, 'избранном')

    @action(methods=['POST', 'DELETE'], detail=True,
            permission_classes=[permissions.IsAuthenticated])
    def shopping_cart(self, request, pk):
        return self.add_delete_item(request, pk, ShoppingCart, 'корзине')

    @action(methods=['GET'], detail=False,
            permission_classes=[permissions.IsAuthenticated])
    def download_shopping_cart(self, request):
        ingredients = Ingredient.objects.filter(
            ingredientamount__recipe__shopping_cart__user=request.user
        ).annotate(total_amount=Sum('ingredientamount__amount'))
        pdf = generate_pdf(ingredients)
        return HttpResponse(
            bytes(pdf.output()), content_type='application/pdf')
