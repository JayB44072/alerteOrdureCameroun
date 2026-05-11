from django.urls import path
from . import views

urlpatterns = [
    path('', views.citoyen_accueil, name='citoyen_accueil'),
    path('signaler/', views.signaler, name='signaler'),
    path('mes-signalements/', views.mes_signalements, name='mes_signalements'),
    path('confirmer/<int:pk>/', views.confirmer, name='confirmer'),
    path('dashboard/', views.hysacam_dashboard, name='hysacam_dashboard'),
    path('traiter/<int:pk>/', views.changer_statut, name='changer_statut'),
]