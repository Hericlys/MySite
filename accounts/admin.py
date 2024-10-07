from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser
from django.utils.translation import gettext_lazy as _


@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    model = CustomUser
    list_display = ('email', 'is_check', 'is_staff', 'is_active',)
    list_editable = ('is_check',)
    list_filter = ('email', 'is_staff', 'is_active',)
    fieldsets = (
        (None, {'fields': ('email', 'first_name', 'last_name', 'password', 'token')}),
        (_('Permissions'), {'fields': ('is_staff', 'is_active', 'is_check')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': (
                'email', 'password1', 'password2', 'is_staff', 'is_active',
                'is_check',
            )}
        ),
    )
    search_fields = ('email',)
    ordering = ('email',)
