from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User

@admin.register(User)
class CustomUserAdmin(UserAdmin):
    list_display = ('username', 'email', 'role', 'ville', 'quartier')
    fieldsets = UserAdmin.fieldsets + (
        ('Informations CleanCity', {'fields': ('role', 'ville', 'quartier')}),
    )