import django_filters as df

from .models import Recipe


class RecipeFilter(df.FilterSet):
    tags = df.AllValuesMultipleFilter(field_name='tags__slug',)
    author = df.NumberFilter(field_name='author', lookup_expr='exact')
    is_favorited = df.NumberFilter(method='get_is_favorited')
    is_in_shopping_cart = df.NumberFilter(method='get_is_in_shopping_cart')

    class Meta:
        model = Recipe
        fields = ['tags', 'author', 'is_favorited', 'is_in_shopping_cart', ]

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
