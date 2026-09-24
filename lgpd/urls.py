from django.urls import path

from . import views

app_name = 'lgpd'

urlpatterns = [
    path('meus-dados/', views.meus_dados, name='meus_dados'),
    path('meus-dados/exportar/', views.exportar_dados, name='exportar_dados'),
    path('meus-dados/excluir/', views.excluir_conta, name='excluir_conta'),
    path('meus-dados/consentimentos/', views.meus_consentimentos, name='meus_consentimentos'),
    path('meus-dados/consentimentos/<int:pk>/revogar/', views.revogar_consentimento, name='revogar_consentimento'),
]