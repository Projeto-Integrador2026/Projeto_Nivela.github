from django.conf import settings
from django.db import models
from django.utils import timezone


class RegistroConsentimento(models.Model):
    """Registra cada consentimento dado (ou revogado) pelo titular (itens 4.4 a 4.7)."""

    class Finalidade(models.TextChoices):
        # Ajustaremos esta lista quando eu vir os dados que o cadastro coleta.
        TERMOS_USO = "termos_uso", "Termos de uso e política de privacidade"
        TELEFONE = "telefone", "Uso do telefone para contato"

    usuario = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="consentimentos",
    )
    finalidade = models.CharField(max_length=30, choices=Finalidade.choices)
    versao_termo = models.CharField(max_length=20)
    concedido = models.BooleanField(default=True)
    data_concessao = models.DateTimeField(default=timezone.now)
    data_revogacao = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ["-data_concessao"]
        verbose_name = "registro de consentimento"
        verbose_name_plural = "registros de consentimento"

    def __str__(self):
        situacao = "concedido" if self.concedido else "revogado"
        return f"{self.usuario} - {self.get_finalidade_display()} ({situacao})"

    def revogar(self):
        """Marca o consentimento como revogado, mantendo o histórico."""
        if self.concedido:
            self.concedido = False
            self.data_revogacao = timezone.now()
            self.save(update_fields=["concedido", "data_revogacao"])


class SolicitacaoTitular(models.Model):
    """Registra os pedidos de direitos do titular (item 4.11).

    Guarda um identificador anônimo para provar o atendimento
    mesmo depois que os dados pessoais forem excluídos.
    """

    class Tipo(models.TextChoices):
        ACESSO = "acesso", "Acesso (consulta) aos dados"
        EXPORTACAO = "exportacao", "Exportação dos dados"
        REVOGACAO = "revogacao", "Revogação de consentimento"
        EXCLUSAO = "exclusao", "Exclusão dos dados"

    class Status(models.TextChoices):
        PENDENTE = "pendente", "Pendente"
        CONCLUIDA = "concluida", "Concluída"

    usuario = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="solicitacoes_lgpd",
    )
    identificador_anonimo = models.CharField(max_length=64, blank=True, default="")
    tipo = models.CharField(max_length=20, choices=Tipo.choices)
    status = models.CharField(
        max_length=20, choices=Status.choices, default=Status.PENDENTE
    )
    data_solicitacao = models.DateTimeField(default=timezone.now)
    data_conclusao = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ["-data_solicitacao"]
        verbose_name = "solicitação do titular"
        verbose_name_plural = "solicitações do titular"

    def __str__(self):
        return f"{self.get_tipo_display()} - {self.get_status_display()}"

    def concluir(self):
        self.status = self.Status.CONCLUIDA
        self.data_conclusao = timezone.now()
        self.save(update_fields=["status", "data_conclusao"])