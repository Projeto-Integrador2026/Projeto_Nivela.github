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


class CadastroView(CreateView):
    """
    Tela de cadastro (link 'Cadastre-se' da tela de login).
    """
    form_class = CadastroForm
    template_name = 'usuarios/cadastro.html'
    success_url = reverse_lazy('two_factor:login')

    def form_valid(self, form):
        # 1. Define a conta como inativa antes de a guardar na base de dados (A-06)
        form.instance.is_active = False
        resposta = super().form_valid(form)

        # 2. Registo explícito do consentimento aos Termos de Uso (mantido)
        RegistroConsentimento.objects.create(
            usuario=self.object,
            finalidade=RegistroConsentimento.Finalidade.TERMOS_USO,
            versao_termo=VERSAO_TERMOS,
            concedido=True,
            data_concessao=timezone.now(),
        )

        # 3. Gerar token seguro de ativação e construir o link
        current_site = get_current_site(self.request)
        uid = urlsafe_base64_encode(force_bytes(self.object.pk))
        token = default_token_generator.make_token(self.object)
        caminho = reverse('ativar_conta', kwargs={'uidb64': uid, 'token': token})
        link_ativacao = f"https://{current_site.domain}{caminho}"

        # 4. Enviar o e-mail (funciona graças à correção do SMTP em produção)
        send_mail(
            subject='Ativação da sua conta no Nivela',
            message=f'Bem-vindo ao Nivela!\n\nPara ativar a sua conta e configurar o 2FA, clique no link abaixo:\n\n{link_ativacao}\n\nSe não solicitou este registo, ignore este e-mail.',
            from_email=None,
            recipient_list=[self.object.email],
        )

        # 5. Avisar o utilizador no ecrã
        messages.success(self.request, 'Conta criada! Verifique o seu e-mail para ativar o acesso.')
        return resposta


class AtivarContaView(View):
    """
    Processa o clique no link de ativação enviado por e-mail.
    """
    def get(self, request, uidb64, token):
        Usuario = get_user_model()
        try:
            uid = force_str(urlsafe_base64_decode(uidb64))
            usuario = Usuario.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, Usuario.DoesNotExist):
            usuario = None

        if usuario is not None and default_token_generator.check_token(usuario, token):
            usuario.is_active = True
            usuario.save()
            messages.success(request, 'A sua conta foi ativada com sucesso! Inicie sessão para configurar o seu autenticador.')
        else:
            messages.error(request, 'O link de ativação é inválido ou já expirou.')
            
        return redirect('two_factor:login')