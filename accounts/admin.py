from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser

class CustomUserAdmin(UserAdmin):
    model = CustomUser
    list_display = ['username', 'email', 'account_type', 'token', 'preferred_language', 'is_staff', 'is_active']
    fieldsets = UserAdmin.fieldsets + (
        (None, {'fields': ('token', 'account_type', 'preferred_language')}),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        (None, {'fields': ('token', 'account_type', 'preferred_language')}),
    )

admin.site.register(CustomUser, CustomUserAdmin)
