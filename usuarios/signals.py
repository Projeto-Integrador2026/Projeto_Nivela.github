"""
Registro de eventos de autenticacao em log (item 5.1 do Requisito 5).

O Django dispara automaticamente os sinais 'user_logged_in' e
'user_logged_out' sempre que alguem entra ou sai do sistema - inclusive
quando o login passa pelo fluxo de 2FA do django-two-factor-auth, ja
que ele chama a funcao padrao de login do Django ao final do processo.
Por isso nao precisamos alterar nenhuma view: so "escutamos" os sinais.
"""
import logging

from django.contrib.auth.signals import user_logged_in, user_logged_out
from django.dispatch import receiver

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
    # 'user' pode vir None em casos raros (ex.: sessao ja invalidada);
    # tratamos para o log nao quebrar por causa disso.
    email = user.email if user is not None else 'desconhecido'
    logger.info(
        f'LOGOUT - usuario: {mascarar_email(email)} - IP: {ip}'
    )