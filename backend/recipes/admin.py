from django.contrib import admin
from django.utils.translation import gettext_lazy as _

from .models import Ingredient, IngredientAmount, Recipe, Tag, Unit

admin.site.site_header = _('Администрирование Foodgram')


class TagAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'color', 'slug',)
    search_fields = ('name',)
    list_filter = ('name',)
    prepopulated_fields = {"slug": ("name",)}
    empty_value_display = _('-пусто-')


class IngredientAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'measurement_unit',)
    search_fields = ('name',)
    list_filter = ('name',)
    empty_value_display = _('-пусто-')


class UnitsAdmin(admin.ModelAdmin):
    list_display = ('id', 'name',)
    search_fields = ('name',)
    list_filter = ('name',)
    empty_value_display = _('-пусто-')


class IngredientAmountInline(admin.TabularInline):
    model = IngredientAmount
    autocomplete_fields = ('ingredient',)
    extra = 2


class RecipeAdmin(admin.ModelAdmin):
    list_display = ('id', 'author', 'ingredient', 'name', 'text',
                    'cooking_time', 'tag',)
    search_fields = ('name', 'text')
    list_filter = ('author', 'name', 'tags')
    empty_value_display = _('-пусто-')
    inlines = (IngredientAmountInline,)
    readonly_fields = ('count_favorite',)

    def ingredient(self, obj):
        return ', '.join([a.name for a in obj.ingredients.all()])

    def tag(self, obj):
        return ', '.join([a.name for a in obj.tags.all()])

    def count_favorite(self, obj):
        return obj.favorite.count()

    ingredient.short_description = _('Ингридиенты')
    tag.short_description = _('Метки')
    count_favorite.short_description = _('Количество добавлений в избранное')


admin.site.register(Unit, UnitsAdmin)
admin.site.register(Tag, TagAdmin)
admin.site.register(Ingredient, IngredientAdmin)
admin.site.register(Recipe, RecipeAdmin)
