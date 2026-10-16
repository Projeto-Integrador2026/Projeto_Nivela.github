"""
Módulo de Mapeamento de URLs da LGPD (Lei Geral de Proteção de Dados - Lei nº 13.709/2018).

Este arquivo define as rotas para o exercício dos direitos dos titulares de dados
(acesso, exportação, exclusão, consulta e revogação de consentimentos) e para a
exibição pública dos documentos legais institucionais (Termos de Uso e Política de Privacidade).
"""

from django.urls import path
from . import views

# Namespace do aplicativo para chamadas de reversão de URL (ex.: 'lgpd:meus_dados')
app_name = 'lgpd'

urlpatterns = [
    # ==============================================================================
    # 1. ROTAS PRIVADAS - DIREITOS DO TITULAR DE DADOS (LGPD, ART. 18)
    # ==============================================================================
    
    # Consulta e confirmação de acesso aos dados pessoais (LGPD, Art. 18, I e II)
    path('meus-dados/', views.meus_dados, name='meus_dados'),
    
    # Portabilidade e download dos dados em formato JSON (LGPD, Art. 18, V)
    path('meus-dados/exportar/', views.exportar_dados, name='exportar_dados'),
    
    # Eliminação definitiva da conta e dados pessoais (LGPD, Art. 18, VI)
    path('meus-dados/excluir/', views.excluir_conta, name='excluir_conta'),
    
    # Gestão e consulta de consentimentos concedidos (LGPD, Art. 8º / Art. 18, IX)
    path('meus-dados/consentimentos/', views.meus_consentimentos, name='meus_consentimentos'),
    
    # Revogação de consentimento específico (LGPD, Art. 8º §5º)
    path(
        'meus-dados/consentimentos/<int:pk>/revogar/',
        views.revogar_consentimento,
        name='revogar_consentimento'
    ),

    # ==============================================================================
    # 2. ROTAS PÚBLICAS - DOCUMENTOS LEGAIS INSTITUCIONAIS (LGPD, ART. 8º E ART. 9º)
    # ==============================================================================
    
    # Termos de Uso do sistema (A-11 / Transparência e Consentimento, Art. 8º)
    path('termos/', views.TermosUsoView.as_view(), name='termos_uso'),
    
    # Política de Privacidade e Tratamento de Dados (A-11 / Transparência, Art. 9º)
    path('privacidade/', views.PoliticaPrivacidadeView.as_view(), name='politica_privacidade'),
]