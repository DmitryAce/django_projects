from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User

class UserAdmin(BaseUserAdmin):
    # Поля, отображаемые в списке пользователей
    list_display = ('email', 'username', 'first_name', 'last_name', 'role', 'last_login', 'is_staff', 'is_active')
    list_filter = ('role', 'is_staff', 'is_superuser', 'is_active', 'last_login') # По каким полям можно филтровать данные

    # Группировка полей по заголовкам, в деталях пользователя
    fieldsets = (
        ('Main', {'fields': ('email', 'password')}),
        ('Personal info', {'fields': ('username', 'first_name', 'last_name', 'role')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Dates', {'fields': ('last_login',)}),
    )

    add_fieldsets = (
        ('Add user', {
            'classes': ('wide',),
            'fields': ('email', 'username', 'password1', 'password2', 'first_name', 'last_name', 'role', 'is_staff', 'is_superuser'),
        }),
    )
    
    # По каким полям будет поиск
    search_fields = ('email', 'username', 'first_name', 'last_name')
    ordering = ('role',)
    filter_horizontal = ('groups', 'user_permissions')

admin.site.register(User, UserAdmin)