from django.contrib import admin
from django.utils.translation import gettext_lazy as _

from .models import User


class UserAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'username', 'email', 'first_name', 'last_name'
    )
    search_fields = ('username', 'email')
    list_filter = ('username', 'email')
    empty_value_display = _('-пусто-')


admin.site.register(User, UserAdmin)
