from django.urls import path

from . import views

app_name = 'lgpd'

urlpatterns = [
    path('meus-dados/consentimentos/', views.meus_consentimentos, name='meus_consentimentos'),
    path('meus-dados/consentimentos/<int:pk>/revogar/', views.revogar_consentimento, name='revogar_consentimento'),
]