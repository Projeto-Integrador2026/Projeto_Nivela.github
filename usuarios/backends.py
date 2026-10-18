"""Backend de autenticacao por e-mail, sem diferenciar maiusculas de minusculas."""
from django.contrib.auth import get_user_model
from django.contrib.auth.backends import ModelBackend


class EmailBackend(ModelBackend):
    """Login por e-mail ignorando maiusculas/minusculas.

    O ModelBackend padrao compara o e-mail exatamente como foi digitado, entao
    "Beatriz@x.com" falhava para a conta "beatriz@x.com" (o teclado do celular
    costuma por a primeira letra maiuscula). Cada falha dessas contava para o
    bloqueio do django-axes. O cadastro ja trata e-mails com iexact; este
    backend faz o login seguir a mesma regra.
    """

    def authenticate(self, request, username=None, password=None, **kwargs):
        Usuario = get_user_model()
        if username is None:
            username = kwargs.get(Usuario.USERNAME_FIELD)
        if username is None or password is None:
            return None
        try:
            user = Usuario._default_manager.get(email__iexact=username.strip())
        except (Usuario.DoesNotExist, Usuario.MultipleObjectsReturned):
            # Gasta o mesmo tempo de um hash real, para o tempo de resposta
            # nao revelar se o e-mail existe.
            Usuario().set_password(password)
            return None
        if user.check_password(password) and self.user_can_authenticate(user):
            return user
        return None
