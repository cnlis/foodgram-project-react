import django_filters as df
from django.db.models import Case, IntegerField, Q, Value, When

from .models import Ingredient, Recipe, Tag


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
    author = df.NumberFilter(field_name='author', lookup_expr='exact')
    is_favorited = df.NumberFilter(method='get_is_favorited')
    is_in_shopping_cart = df.NumberFilter(method='get_is_in_shopping_cart')

    class Meta:
        model = Recipe
        fields = ('tags', 'author', 'is_favorited', 'is_in_shopping_cart', )

    def get_is_favorited(self, queryset, name, value):
        user = self.request.user
        if value == 1 and user.is_authenticated:
            return queryset.filter(favorite__user=user)
        return queryset

    def get_is_in_shopping_cart(self, queryset, name, value):
        user = self.request.user
        if value == 1 and user.is_authenticated:
            return queryset.filter(shopping_cart__user=user)
        return queryset
