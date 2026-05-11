from django.contrib import admin
from .models import Quartier, Signalement, Confirmation

@admin.register(Quartier)
class QuartierAdmin(admin.ModelAdmin):
    list_display = ('nom', 'ville')

@admin.register(Signalement)
class SignalementAdmin(admin.ModelAdmin):
    list_display = ('auteur', 'quartier', 'statut', 'date_creation')
    list_filter = ('statut', 'quartier')

@admin.register(Confirmation)
class ConfirmationAdmin(admin.ModelAdmin):
    list_display = ('signalement', 'utilisateur', 'date')