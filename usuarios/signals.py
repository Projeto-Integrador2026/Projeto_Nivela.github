"""
Registro de eventos de autenticacao em log (itens 5.1 e 5.2 do Requisito 5).

O Django e as bibliotecas de 2FA disparam sinais automaticamente para
cada evento de autenticacao - login/logout com sucesso, falha de
senha e falha/sucesso do codigo 2FA. Por isso nao precisamos alterar
nenhuma view: so "escutamos" os sinais.
"""
import logging

from django.contrib.auth.signals import (
    user_logged_in,
    user_logged_out,
    user_login_failed,
)
from django.dispatch import receiver
from django_otp.forms import otp_verification_failed
from two_factor.signals import user_verified

from lgpd.utils import mascarar_email
from .utils import obter_ip_cliente

# Logger configurado em settings.py (LOGGING), grava em logs/autenticacao.log
logger = logging.getLogger('usuarios.autenticacao')


@receiver(user_logged_in)
def registrar_login(sender, request, user, **kwargs):
    """Registra em log todo login concluido com sucesso (item 5.1)."""
    ip = obter_ip_cliente(request)
    logger.info(
        f'LOGIN bem-sucedido - usuario: {mascarar_email(user.email)} - IP: {ip}'
    )


@receiver(user_logged_out)
def registrar_logout(sender, request, user, **kwargs):
    """Registra em log todo logout (item 5.1)."""
    ip = obter_ip_cliente(request)
    email = user.email if user is not None else 'desconhecido'
    logger.info(
        f'LOGOUT - usuario: {mascarar_email(email)} - IP: {ip}'
    )


@receiver(user_login_failed)
def registrar_falha_login(sender, credentials, request=None, **kwargs):
    """Registra em log toda falha de login por e-mail/senha errados (item 5.2).

    Tambem dispara quando a conta esta bloqueada pelo django-axes, entao
    esse log serve tanto pra tentativa errada quanto pra bloqueio ativo.
    """
    # O Django guarda o e-mail digitado sob a chave 'username', mesmo o
    # projeto usando login por e-mail (USERNAME_FIELD = 'email').
    email_tentado = credentials.get('username') if credentials else None
    ip = obter_ip_cliente(request)
    logger.warning(
        f'FALHA no login - usuario: {mascarar_email(email_tentado)} - IP: {ip}'
    )


@receiver(otp_verification_failed)
def registrar_falha_2fa(sender, user, **kwargs):
    """Registra em log toda falha no codigo do 2FA (item 5.2).

    Este sinal do django_otp nao traz o 'request' junto, entao aqui nao
    temos como saber o IP de quem errou o codigo - so o usuario.
    """
    logger.warning(
        f'FALHA no codigo 2FA - usuario: {mascarar_email(user.email)}'
    )


@receiver(user_verified)
def registrar_sucesso_2fa(sender, request, user, device, **kwargs):
    """Registra em log a validacao com sucesso do codigo 2FA (item 5.2)."""
    ip = obter_ip_cliente(request)
    logger.info(
        f'2FA validado com sucesso - usuario: {mascarar_email(user.email)} '
        f'- dispositivo: {device.__class__.__name__} - IP: {ip}'
    )