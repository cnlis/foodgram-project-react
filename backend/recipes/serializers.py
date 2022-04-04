from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from users.serializers import CustomUserSerializer

from .fields import Base64ImageField
from .models import Ingredient, IngredientAmount, Recipe, Tag

User = get_user_model()


class TagSerializer(serializers.ModelSerializer):

    class Meta:
        model = Tag
        fields = '__all__'


class IngredientAmountWriteSerializer(serializers.ModelSerializer):
    id = serializers.PrimaryKeyRelatedField(queryset=Ingredient.objects.all())
    amount = serializers.IntegerField(min_value=1, max_value=1000)

    class Meta:
        model = IngredientAmount
        exclude = ('recipe', 'ingredient',)


class IngredientAmountReadSerializer(serializers.ModelSerializer):
    id = serializers.ReadOnlyField(source='ingredient.id')
    name = serializers.ReadOnlyField(source='ingredient.name')
    measurement_unit = serializers.ReadOnlyField(
        source='ingredient.measurement_unit.name'
    )

    class Meta:
        model = IngredientAmount
        exclude = ('recipe', 'ingredient',)


class IngredientSerializer(serializers.ModelSerializer):
    measurement_unit = serializers.CharField(
        source='measurement_unit.name'
    )

    class Meta:
        model = Ingredient
        fields = '__all__'


class RecipeSerializer(serializers.ModelSerializer):
    ingredients = IngredientAmountReadSerializer(
        source='ingredientamount_set',
        many=True,
        read_only=True
    )
    tags = TagSerializer(many=True, read_only=True)
    image = Base64ImageField(required=True)
    name = serializers.CharField(required=True)
    text = serializers.CharField(required=True)
    cooking_time = serializers.IntegerField(required=True)
    author = CustomUserSerializer(default=serializers.CurrentUserDefault())
    is_favorited = serializers.SerializerMethodField()
    is_in_shopping_cart = serializers.SerializerMethodField()

    class Meta:
        model = Recipe
        fields = '__all__'

    def get_is_favorited(self, obj):
        user = self.context.get('request').user
        if user.is_anonymous:
            return False
        return user.favorite.filter(recipe=obj).exists()

    def get_is_in_shopping_cart(self, obj):
        user = self.context.get('request').user
        if user.is_anonymous:
            return False
        return user.shopping_cart.filter(recipe=obj).exists()

    def check_data(self, data, field_name, count_message, unique_message):
        if not data:
            raise ValidationError({field_name: [count_message]})
        data_set = set()
        for item in data:
            if isinstance(item, dict):
                item = item.get('id')
            if item in data_set:
                raise ValidationError({field_name: [unique_message]})
            data_set.add(item)

    def validate(self, data):
        tags = self.initial_data.pop('tags', None)
        self.check_data(
            data=tags,
            field_name='tags',
            count_message=_('В рецепте должна быть минимум одна метка'),
            unique_message=_('Все метки должны быть уникальны')
        )
        for tag_pk in tags:
            if not Tag.objects.filter(pk=tag_pk).exists():
                raise ValidationError({'tags': [_('Метка не существует')]})
        data['tags'] = tags
        ingredients = self.initial_data.pop('ingredients', None)
        self.check_data(
            data=ingredients,
            field_name='ingredients',
            count_message=_('В рецепте должен быть минимум один ингредиент'),
            unique_message=_('Все ингредиенты должны быть уникальны'),
        )
        serializer = IngredientAmountWriteSerializer(
            data=ingredients,
            many=True,
        )
        serializer.is_valid(raise_exception=True)
        data['ingredients'] = ingredients
        return data

    def add_ingredients(self, obj, data):
        for item in data:
            IngredientAmount.objects.create(
                recipe=obj,
                ingredient_id=item.get('id'),
                amount=item.get('amount')
            )

    def create(self, validated_data):
        tags = validated_data.pop('tags')
        ingredients = validated_data.pop('ingredients')
        recipe = Recipe.objects.create(**validated_data)
        recipe.tags.set(tags)
        self.add_ingredients(recipe, ingredients)
        return recipe

    def update(self, instance, validated_data):
        instance.image = validated_data.get('image', instance.image)
        instance.name = validated_data.get('name', instance.name)
        instance.text = validated_data.get('text', instance.text)
        instance.cooking_time = validated_data.get(
            'cooking_time', instance.cooking_time
        )
        tags = validated_data.get('tags', instance.tags)
        ingredients = validated_data.get('ingredients', instance.ingredients)
        instance.tags.clear()
        instance.tags.set(tags)
        IngredientAmount.objects.filter(recipe=instance).delete()
        self.add_ingredients(instance, ingredients)
        instance.save()
        return instance


class ShortRecipeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Recipe
        fields = ('id', 'name', 'image', 'cooking_time',)


class SubscribeSerializer(CustomUserSerializer):
    recipes = serializers.SerializerMethodField()
    recipes_count = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ('email', 'id', 'username', 'first_name', 'last_name',
                  'is_subscribed', 'recipes', 'recipes_count',)

    def get_recipes(self, obj):
        recipes_limit = self.context.get('request').GET.get('recipes_limit')
        queryset = obj.recipe.all()
        if recipes_limit:
            queryset = queryset[:int(recipes_limit)]
        return ShortRecipeSerializer(queryset, many=True).data

    def get_recipes_count(self, obj):
        return obj.recipe.count()
