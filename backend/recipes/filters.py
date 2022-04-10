import django_filters as df
from django.contrib.auth import get_user_model
from django.db.models import Case, IntegerField, Q, Value, When

from .cart import Cart
from .models import Ingredient, Recipe, Tag

User = get_user_model()


STATUS_CHOICES = (
    (0, '0'),
    (1, '1'),
)


class IngredientFilter(df.FilterSet):
    name = df.CharFilter(method='get_name')

    class Meta:
        model = Ingredient
        fields = ('name', )

    def get_name(self, queryset, name, value):
        q1 = Q(name__istartswith=value)
        q2 = Q(name__icontains=value)
        return queryset.filter(q1 | q2).annotate(
            search_ordering=Case(
                When(q1, then=Value(2)),
                When(q2, then=Value(1)),
                default=Value(-1),
                output_field=IntegerField(),
            )).order_by('-search_ordering')


class RecipeFilter(df.FilterSet):
    tags = df.ModelMultipleChoiceFilter(
        field_name='tags__slug',
        to_field_name='slug',
        queryset=Tag.objects.all(),
    )
    author = df.ModelChoiceFilter(queryset=User.objects.all())
    is_favorited = df.ChoiceFilter(
        method='get_is_favorited', choices=STATUS_CHOICES)
    is_in_shopping_cart = df.ChoiceFilter(
        method='get_is_in_shopping_cart', choices=STATUS_CHOICES)

    class Meta:
        model = Recipe
        fields = ('tags', 'author', 'is_favorited', 'is_in_shopping_cart', )

    def get_is_favorited(self, queryset, name, value):
        user = self.request.user
        if value == '1' and user.is_authenticated:
            return queryset.filter(favorite__user=user)
        return queryset

    def get_is_in_shopping_cart(self, queryset, name, value):
        user = self.request.user
        if value == '1':
            if user.is_authenticated:
                return queryset.filter(shopping_cart__user=user)
            cart = Cart(self.request)
            return queryset.filter(pk__in=cart)
        return queryset
