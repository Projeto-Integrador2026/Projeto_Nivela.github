from django.contrib import admin

from .models import RegistroConsentimento, SolicitacaoTitular


@admin.register(RegistroConsentimento)
class RegistroConsentimentoAdmin(admin.ModelAdmin):
    list_display = ("usuario", "finalidade", "versao_termo", "concedido",
                    "data_concessao", "data_revogacao")
    list_filter = ("finalidade", "concedido")


@admin.register(SolicitacaoTitular)
class SolicitacaoTitularAdmin(admin.ModelAdmin):
    list_display = ("tipo", "status", "data_solicitacao", "data_conclusao")
    list_filter = ("tipo", "status")