from django.db.models import Sum
from django.http import HttpResponse
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import mixins, permissions, viewsets
from rest_framework.decorators import action
from rest_framework.generics import get_object_or_404

from .cart import Cart
from .filters import IngredientFilter, RecipeFilter
from .mixins import ResponseMixin
from .models import Favorite, Ingredient, Recipe, ShoppingCart, Tag
from .permissions import IsAuthorOrReadOnly
from .serializers import IngredientSerializer, RecipeSerializer, TagSerializer
from .utilities import generate_pdf


class ReadOnlyViewSet(mixins.RetrieveModelMixin, mixins.ListModelMixin,
                      viewsets.GenericViewSet):
    permission_classes = (permissions.AllowAny,)


class TagViewSet(ReadOnlyViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    pagination_class = None


class IngredientViewSet(ReadOnlyViewSet):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    filter_backends = (DjangoFilterBackend,)
    filterset_class = IngredientFilter
    pagination_class = None


class RecipeViewSet(ResponseMixin, viewsets.ModelViewSet):
    """
    Работа с рецептами, подписками на них, добавления в корзину и
    экспорта покупок в PDF.
    """

    queryset = Recipe.objects.all()
    permission_classes = (IsAuthorOrReadOnly,)
    serializer_class = RecipeSerializer
    filter_backends = (DjangoFilterBackend,)
    filterset_class = RecipeFilter

    def session_add_delete_item(self, request, recipe):
        cart = Cart(request)
        cart_len = len(cart)
        if request.method == 'DELETE':
            cart.remove(recipe)
            deleted = cart_len != len(cart)
            return self.delete_response(deleted, recipe)
        cart.add(recipe)
        created = cart_len != len(cart)
        return self.create_response(created, recipe, self.get_serializer)

    def add_delete_item(self, request, recipe, model):
        user = request.user
        if request.method == 'DELETE':
            deleted, _ = model.objects.filter(
                user=user, recipe=recipe).delete()
            return self.delete_response(deleted, recipe)
        _, created = model.objects.get_or_create(user=user, recipe=recipe)
        return self.create_response(created, recipe, self.get_serializer)

    @action(methods=['POST', 'DELETE'], detail=True,
            permission_classes=[permissions.IsAuthenticated])
    def favorite(self, request, pk):
        recipe = get_object_or_404(Recipe, pk=pk)
        return self.add_delete_item(request, recipe, Favorite)

    @action(methods=['POST', 'DELETE'], detail=True,
            permission_classes=[permissions.AllowAny])
    def shopping_cart(self, request, pk):
        recipe = get_object_or_404(Recipe, pk=pk)
        if not request.user.is_authenticated:
            return self.session_add_delete_item(request, recipe)
        return self.add_delete_item(request, recipe, ShoppingCart)

    @action(methods=['GET'], detail=False,
            permission_classes=[permissions.AllowAny])
    def download_shopping_cart(self, request):
        if request.user.is_authenticated:
            ingredients = Ingredient.objects.filter(
                amount__recipe__shopping_cart__user=request.user
            ).annotate(total_amount=Sum('amount__amount'))
        else:
            cart = Cart(request)
            ingredients = Ingredient.objects.filter(
                amount__recipe__pk__in=cart
            ).annotate(total_amount=Sum('amount__amount'))
        pdf = generate_pdf(ingredients)
        return HttpResponse(
            bytes(pdf.output()), content_type='application/pdf')
