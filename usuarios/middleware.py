from django.contrib.auth.views import redirect_to_login
from django.shortcuts import redirect
from django_otp.plugins.otp_totp.models import TOTPDevice


class LoginRequiredMiddleware:
    """
    Exige login em todo o site (default-deny). Qualquer rota nova ja nasce
    protegida; so ficam abertas as listadas em PREFIXOS_PUBLICOS.
    """

    # Prefixos de URL acessiveis SEM estar logado
    PREFIXOS_PUBLICOS = [
        '/account/',          # login, 2FA e demais telas do django-two-factor-auth
        '/cadastro/',         # criar conta
        '/recuperar-senha/',  # as 4 telas da recuperacao de senha
        '/admin/',            # o admin tem login proprio
        '/static/',
        '/media/',
        '/favicon.ico',       # o navegador pede sozinho; nao pode ser redirecionado
    ]

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if not request.user.is_authenticated:
            publico = any(request.path.startswith(p) for p in self.PREFIXOS_PUBLICOS)
            if not publico:
                # Manda para o login e guarda a pagina pedida em ?next=
                return redirect_to_login(request.get_full_path())

        return self.get_response(request)


class Force2FASetupMiddleware:
    """
    Obriga todo usuario autenticado a configurar o 2FA (TOTP) antes de
    acessar qualquer outra parte do sistema, caso ainda nao tenha
    nenhum dispositivo confirmado. Atende ao RF07/RF08 (2FA obrigatorio).
    """

    # Prefixos de URL que o usuario PRECISA conseguir acessar mesmo sem 2FA configurado
    PREFIXOS_PERMITIDOS = [
        '/account/',   # todo o fluxo do django-two-factor-auth (login, setup, qr, logout)
        '/admin/logout/',
        '/sair/',      # logout do app usuarios
        '/static/',
        '/media/',
        '/favicon.ico',   # o navegador pede sozinho; nao pode ser redirecionado
    ]

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.user.is_authenticated:
            tem_dispositivo = TOTPDevice.objects.filter(
                user=request.user, confirmed=True
            ).exists()

            if not tem_dispositivo:
                caminho = request.path
                permitido = any(caminho.startswith(p) for p in self.PREFIXOS_PERMITIDOS)
                if not permitido:
                    return redirect('/account/two_factor/setup/')

        return self.get_response(request)