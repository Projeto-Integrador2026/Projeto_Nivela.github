from django.utils import timezone
from lgpd.inventario import VERSAO_TERMOS
from lgpd.models import RegistroConsentimento
from django.shortcuts import render
import logging
from django.contrib.auth.views import PasswordResetView, PasswordResetConfirmView
from django.urls import reverse_lazy
from django.views.generic import CreateView
from lgpd.utils import mascarar_email
from .forms import CadastroForm


# Views customizadas para o Requisito 2 - Recuperacao de Senha

# Logger customizado para recuperacao de senha (itens 2.6 e 2.7)
# Configurado em settings.py (LOGGING), grava no arquivo logs/recuperacao_senha.log
logger = logging.getLogger('usuarios.recuperacao_senha')


class RecuperarSenhaView(PasswordResetView):
    """
    View customizada que estende a PasswordResetView do Django
    apenas para registrar em log toda solicitacao de recuperacao (item 2.6).

    Toda a logica de geracao do token seguro (item 2.2) e envio do email
    e herdada da PasswordResetView original do Django - so adicionamos o log.
    """
    def form_valid(self, form):
        # form_valid roda quando o email informado passa na validacao do formulario
        # (nao significa necessariamente que o email existe no banco - por seguranca,
        # o Django nao revela isso ao usuario)
        email = form.cleaned_data.get('email')

        # Registra a solicitacao de recuperacao em log (item 2.6)
        logger.info(f'Solicitacao de recuperacao de senha para o email: {mascarar_email(email)}')

        # Chama o comportamento padrao do Django: gera o token e envia o email
        return super().form_valid(form)


class RedefinirSenhaView(PasswordResetConfirmView):
    """
    View customizada que estende a PasswordResetConfirmView do Django
    para registrar em log o sucesso ou falha da redefinicao de senha (item 2.7).

    A validacao do token (se e valido, se nao expirou, se ja foi usado -
    itens 2.3, 2.4 e 2.5) e feita automaticamente pela view original do Django
    antes mesmo de chegar aqui, atraves da variavel 'validlink' no template.
    """
    def form_valid(self, form):
        # form_valid roda quando a nova senha informada e valida e foi salva com sucesso
        # Registra o SUCESSO da redefinicao em log (item 2.7)
        logger.info(f'Senha redefinida com SUCESSO para o usuario: {mascarar_email(form.user.email)}')

        return super().form_valid(form)

    def form_invalid(self, form):
        # form_invalid roda quando a nova senha nao passa na validacao
        # (ex: muito curta, muito comum, so numeros - ver AUTH_PASSWORD_VALIDATORS)
        # Registra a FALHA da redefinicao em log (item 2.7)
        logger.warning(f'FALHA ao redefinir senha para o usuario: {mascarar_email(form.user.email)}')

        return super().form_invalid(form)

# Cadastro de novos usuarios


class CadastroView(CreateView):
    """
    Tela de cadastro (link 'Cadastre-se' da tela de login).

    A senha e gravada com hash (PBKDF2) pelo UserCreationForm e passa
    pelos validadores de AUTH_PASSWORD_VALIDATORS. Depois de cadastrar,
    o usuario e enviado para a tela de login.
    """
    form_class = CadastroForm
    template_name = 'usuarios/cadastro.html'
    success_url = reverse_lazy('two_factor:login')

    def form_valid(self, form):
        resposta = super().form_valid(form)

        # Registro explícito do consentimento aos Termos de Uso (item 4.4),
        # já associado à finalidade "termos_uso" e à versão vigente do
        # termo no momento do cadastro.
        RegistroConsentimento.objects.create(
            usuario=self.object,
            finalidade=RegistroConsentimento.Finalidade.TERMOS_USO,
            versao_termo=VERSAO_TERMOS,
            concedido=True,
            data_concessao=timezone.now(),
        )

        return resposta