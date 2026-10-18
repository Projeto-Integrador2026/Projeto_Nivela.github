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
from django.contrib.sites.shortcuts import get_current_site
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.core.mail import send_mail
from django.contrib.auth.tokens import default_token_generator
from django.contrib import messages
from django.contrib.auth import get_user_model
from django.views import View
from django.shortcuts import redirect
from django.urls import reverse

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

MSG_CADASTRO = ('Cadastro recebido! Faça login para configurar o seu autenticador (2FA). '
                'Se este e-mail já tinha conta, entre com a senha original.')


class CadastroView(CreateView):
    """
    Tela de cadastro (link 'Cadastre-se' da tela de login).

    DECISAO DO GRUPO: a conta nasce ATIVA e o e-mail NAO e verificado, porque o
    plano gratuito do Render bloqueia o SMTP (portas 25/465/587) e o e-mail de
    ativacao nunca chegava. Risco aceito: qualquer pessoa pode cadastrar o
    e-mail de outra.

    Se o e-mail ja existe, a tela responde igual a um cadastro novo (A-04).
    """
    form_class = CadastroForm
    template_name = 'usuarios/cadastro.html'
    success_url = reverse_lazy('two_factor:login')

    def post(self, request, *args, **kwargs):
        email_digitado = (request.POST.get('email') or '').strip()
        Usuario = get_user_model()

        # iexact: "A@x.com" e "a@x.com" sao a mesma pessoa
        existente = None
        if email_digitado:
            existente = Usuario.objects.filter(email__iexact=email_digitado).first()

        if existente is None:
            return super().post(request, *args, **kwargs)

        # E-mail ja cadastrado: valida o resto do formulario (senha, termos) para
        # que a resposta seja IDENTICA a de um e-mail novo, sem revelar nada.
        self.object = None  # exigido pelo CreateView ao reexibir o formulario
        form = self.get_form()
        form.is_valid()
        form.errors.pop('email', None)  # esconde o "ja existe uma conta com este e-mail"
        if form.errors:
            return self.form_invalid(form)

        messages.success(request, MSG_CADASTRO)
        return redirect(self.success_url)

    def form_valid(self, form):
        resposta = super().form_valid(form)  # is_active=True (padrao do Django)

        # Consentimento aos Termos de Uso
        RegistroConsentimento.objects.create(
            usuario=self.object,
            finalidade=RegistroConsentimento.Finalidade.TERMOS_USO,
            versao_termo=VERSAO_TERMOS,
            concedido=True,
            data_concessao=timezone.now(),
        )

        messages.success(self.request, MSG_CADASTRO)
        return resposta
