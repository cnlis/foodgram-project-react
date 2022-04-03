from django.contrib.auth import get_user_model
from django.core.validators import (MaxLengthValidator, MaxValueValidator,
                                    MinValueValidator)
from django.db import models
from django.db.models import UniqueConstraint
from django.utils.translation import gettext_lazy as _

User = get_user_model()


class Tag(models.Model):
    name = models.CharField(
        max_length=50,
        unique=True,
        verbose_name=_('Название'),
    )
    color = models.CharField(
        max_length=7,
        unique=True,
        verbose_name=_('Цвет'),
    )
    slug = models.SlugField(
        max_length=50,
        unique=True,
        verbose_name=_('Слаг'),
    )

    class Meta:
        verbose_name = _('Метка')
        verbose_name_plural = _('Метки')

    def __str__(self):
        return f'{self.name}'


class Unit(models.Model):
    name = models.CharField(
        max_length=50,
        unique=True,
        verbose_name=_('Название'),
    )

    class Meta:
        ordering = ['name']
        verbose_name = _('Единица измерения')
        verbose_name_plural = _('Единицы измерения')

    def __str__(self):
        return f'{self.name}'


class Ingredient(models.Model):
    name = models.CharField(max_length=100, verbose_name=_('Название'),)
    measurement_unit = models.ForeignKey(
        Unit,
        on_delete=models.SET_NULL,
        related_name='ingredient',
        null=True,
        verbose_name=_('Единица измерения'),
    )

    class Meta:
        verbose_name = _('Ингредиент')
        verbose_name_plural = _('Ингредиенты')

    def __str__(self):
        return f'{self.name} ({self.measurement_unit.name})'


class IngredientAmount(models.Model):
    recipe = models.ForeignKey('Recipe', on_delete=models.CASCADE)
    ingredient = models.ForeignKey(Ingredient, on_delete=models.CASCADE)
    amount = models.IntegerField(
        default=1,
        validators=[MinValueValidator(1), MaxValueValidator(1000)],
        verbose_name=_('Количество')
    )

    class Meta:
        constraints = [
            UniqueConstraint(
                fields=['recipe', 'ingredient'],
                name='unique_ingredient'
            ),
        ]
        ordering = ['-id']
        verbose_name = _('Ингредиент')
        verbose_name_plural = _('Список ингредиентов')

    def __str__(self):
        return (_('В рецепте {} {} {}')
                .format(self.recipe, self.amount, self.ingredient))


class Recipe(models.Model):
    tags = models.ManyToManyField(Tag, verbose_name=_('Метки'))
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='recipe',
        verbose_name=_('Автор'),
    )
    ingredients = models.ManyToManyField(
        Ingredient,
        through=IngredientAmount,
        verbose_name=_('Ингридиенты')
    )
    name = models.CharField(max_length=200, verbose_name=_('Название'))
    text = models.TextField(
        max_length=1000,
        validators=[MaxLengthValidator(1000)],
        verbose_name=_('Описание')
    )
    image = models.ImageField(verbose_name=_('Изображение'))
    cooking_time = models.IntegerField(
        default=1,
        validators=[MinValueValidator(1), MaxValueValidator(1440)],
        verbose_name=_('Время приготовления')
    )

    class Meta:
        ordering = ['-id']
        verbose_name = _('Рецепт')
        verbose_name_plural = _('Рецепты')

    def __str__(self):
        return f'{self.name}'


class Favorite(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='favorite',
        verbose_name=_('Пользователь')
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='favorite',
        verbose_name=_('Рецепт')
    )

    class Meta:
        constraints = [
            UniqueConstraint(
                fields=['user', 'recipe'],
                name='unique_favorite'
            ),
        ]
        ordering = ['-id']
        verbose_name = _('Избранное')
        verbose_name_plural = _('Избранные')

    def __str__(self):
        return (_('Пользователь {} добавил в избранное {}')
                .format(self.user, self.recipe))


class ShoppingCart(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='shopping_cart',
        verbose_name=_('Пользователь')
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='shopping_cart',
        verbose_name=_('Рецепт')
    )

    class Meta:
        constraints = [
            UniqueConstraint(
                fields=['user', 'recipe'],
                name='unique_cart'
            ),
        ]
        ordering = ['-id']
        verbose_name = _('Список покупок')
        verbose_name_plural = _('Списки покупок')

    def __str__(self):
        return (_('Пользователь {} добавил в корзину {}')
                .format(self.user, self.recipe))
