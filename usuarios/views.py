import logging

from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth.views import PasswordResetConfirmView, PasswordResetView
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.utils import timezone
from django.views.generic import CreateView

from lgpd.inventario import VERSAO_TERMOS
from lgpd.models import RegistroConsentimento
from lgpd.utils import mascarar_email

from .forms import CadastroForm
from .utils import obter_ip_cliente

# Views customizadas para o Requisito 2 - Recuperacao de Senha

# Logger customizado para recuperacao de senha (itens 2.6 e 2.7)
# Configurado em settings.py (LOGGING), grava no arquivo logs/recuperacao_senha.log
logger = logging.getLogger('usuarios.recuperacao_senha')


class RecuperarSenhaView(PasswordResetView):
    """
    View customizada que estende a PasswordResetView do Django para registrar
    em log toda solicitacao de recuperacao, com o IP (item 2.6).

    Toda a logica de geracao do token seguro (item 2.2) e envio do e-mail
    e herdada da PasswordResetView original do Django. No Django 5.2.17 uma
    falha de SMTP nao derruba a requisicao (o teste
    test_falha_no_envio_do_email_nao_gera_erro_500 protege esse comportamento).
    """
    def form_valid(self, form):
        # form_valid roda quando o e-mail passa na validacao do formulario
        # (nao significa que o e-mail existe no banco - o Django nao revela isso)
        email = form.cleaned_data.get('email')

        # Registra a solicitacao de recuperacao em log (item 2.6)
        logger.info(
            f'Solicitacao de recuperacao de senha para o email: '
            f'{mascarar_email(email)} - IP: {obter_ip_cliente(self.request)}'
        )

        # Comportamento padrao do Django: gera o token e envia o e-mail
        return super().form_valid(form)


class RedefinirSenhaView(PasswordResetConfirmView):
    """
    View customizada que estende a PasswordResetConfirmView do Django
    para registrar em log o sucesso ou falha da redefinicao de senha (item 2.7).

    A validacao do token (se e valido, se nao expirou, se ja foi usado -
    itens 2.3, 2.4 e 2.5) e feita pela view original do Django, atraves da
    variavel 'validlink' no template.
    """
    def get_context_data(self, **kwargs):
        contexto = super().get_context_data(**kwargs)
        # Link invalido, expirado ou ja usado: a view do Django nao chama
        # form_invalid nesse caso, entao o registro e feito aqui (item 2.7)
        if not contexto.get('validlink'):
            logger.warning(
                'FALHA ao redefinir senha: link invalido, expirado ou ja usado '
                f'- IP: {obter_ip_cliente(self.request)}'
            )
        return contexto

    def form_valid(self, form):
        # Nova senha aceita e salva: registra o SUCESSO (item 2.7)
        logger.info(
            f'Senha redefinida com SUCESSO para o usuario: '
            f'{mascarar_email(form.user.email)} - IP: {obter_ip_cliente(self.request)}'
        )
        return super().form_valid(form)

    def form_invalid(self, form):
        # Nova senha rejeitada pelos validadores (muito curta, comum, so numeros
        # - ver AUTH_PASSWORD_VALIDATORS): registra a FALHA (item 2.7)
        logger.warning(
            f'FALHA ao redefinir senha para o usuario: '
            f'{mascarar_email(form.user.email)} - IP: {obter_ip_cliente(self.request)}'
        )
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