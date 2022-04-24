from django.contrib.auth import get_user_model
from django.db.models import Case, IntegerField, Q, Value, When
from django_filters import rest_framework as df

from .cart import Cart
from .models import Ingredient, Tag

User = get_user_model()


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
    is_favorited = df.BooleanFilter()
    is_in_shopping_cart = df.BooleanFilter(method='get_is_in_shopping_cart')

    class Meta:
        fields = ('tags', 'author', 'is_favorited', 'is_in_shopping_cart', )

    def get_is_in_shopping_cart(self, queryset, name, value):
        user = self.request.user
        if value:
            if user.is_authenticated:
                return queryset.filter(is_in_shopping_cart=True)
            cart = Cart(self.request)
            return queryset.filter(pk__in=cart)
        return queryset
