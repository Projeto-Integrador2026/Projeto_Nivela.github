"""
Middlewares do Módulo de Usuários para Controle de Acesso e Segurança.

Este arquivo implementa a política de controle de acesso baseada no princípio
de "Default-Deny" (OWASP A01:2021 - Broken Access Control) e a obrigatoriedade
da configuração de Autenticação em Dois Fatores (2FA/TOTP) para usuários autenticados (RF07/RF08).
"""

from typing import Callable
from django.contrib.auth.views import redirect_to_login
from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect
from django_otp.plugins.otp_totp.models import TOTPDevice


class LoginRequiredMiddleware:
    """
    Middleware de Controle de Acesso Global (Default-Deny).

    Exige autenticação em todo o sistema por padrão. Qualquer nova rota criada
    já nasce restrita, sendo liberadas apenas as rotas explicitamente declaradas
    em PREFIXOS_PUBLICOS.
    """

    # Lista imutável de prefixos de URL acessíveis publicamente (sem autenticação)
    PREFIXOS_PUBLICOS = (
        '/account/',          # Telas de login, 2FA e perfil (django-two-factor-auth)
        '/cadastro/',         # Tela de criação de novas contas
        '/recuperar-senha/',  # Fluxo de recuperação de senha por e-mail
        '/admin/',            # Área administrativa (possui fluxo de autenticação próprio)
        '/termos/',           # Documentos legais da LGPD (A-11)
        '/privacidade/',      # Documentos legais da LGPD (A-11)
        '/static/',           # Arquivos estáticos (CSS, JS, imagens)
        '/media/',            # Arquivos de mídia
        '/favicon.ico',       # Ícone do navegador
    )

    def __init__(self, get_response: Callable[[HttpRequest], HttpResponse]) -> None:
        self.get_response = get_response

    def __call__(self, request: HttpRequest) -> HttpResponse:
        if not request.user.is_authenticated:
            # Normalização da URL para prevenir redirecionamentos incorretos quando
            # a rota pública é acessada sem a barra final (Correção do Achado A-25)
            caminho = request.path if request.path.endswith('/') else f"{request.path}/"

            # Verifica se o caminho requisitado pertence a algum prefixo público
            publico = any(caminho.startswith(p) for p in self.PREFIXOS_PUBLICOS)

            if not publico:
                # Redireciona para o login e preserva a URL de destino no parâmetro ?next=
                return redirect_to_login(request.get_full_path())

        return self.get_response(request)


class Force2FASetupMiddleware:
    """
    Middleware para Obrigatoriedade do Segundo Fator de Autenticação (2FA/TOTP).

    Redireciona todo usuário autenticado que ainda não configurou um dispositivo
    TOTP verificado para a tela de setup do 2FA, impedindo o acesso a outras áreas
    da aplicação (Atende aos Requisitos RF07/RF08).
    """

    # Prefixos de URL que o usuário inativo/sem 2FA precisa acessar obrigatoriamente
    PREFIXOS_PERMITIDOS = (
        '/account/',      # Fluxo completo do 2FA (setup, QR code, validação e logout)
        '/admin/logout/', # Permite encerrar sessão administrativa
        '/sair/',         # Permite encerrar sessão da aplicação
        '/static/',       # Estilos e scripts necessários para renderização da tela de setup
        '/media/',        # Arquivos de mídia
        '/favicon.ico',   # Requisição automática do navegador
    )

    def __init__(self, get_response: Callable[[HttpRequest], HttpResponse]) -> None:
        self.get_response = get_response

    def __call__(self, request: HttpRequest) -> HttpResponse:
        if request.user.is_authenticated:
            # Verifica no banco de dados se o usuário possui dispositivo TOTP confirmado
            tem_dispositivo = TOTPDevice.objects.filter(
                user=request.user, confirmed=True
            ).exists()

            if not tem_dispositivo:
                # Normalização do caminho (A-25)
                caminho = request.path if request.path.endswith('/') else f"{request.path}/"
                permitido = any(caminho.startswith(p) for p in self.PREFIXOS_PERMITIDOS)

                if not permitido:
                    # Força o redirecionamento para o setup do 2FA
                    return redirect('/account/two_factor/setup/')

        return self.get_response(request)