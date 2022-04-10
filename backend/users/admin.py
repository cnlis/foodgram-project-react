from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import gettext_lazy as _

User = get_user_model()


class CustomUserAdmin(UserAdmin):
    list_display = (
        'id', 'username', 'email', 'first_name', 'last_name'
    )
    search_fields = ('username', 'email')
    list_filter = ('username', 'email')
    empty_value_display = _('-пусто-')


admin.site.register(User, CustomUserAdmin)
