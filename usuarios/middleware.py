from django.shortcuts import redirect
from django_otp.plugins.otp_totp.models import TOTPDevice


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
        '/static/',
        '/media/',
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