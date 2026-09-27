from django.apps import AppConfig


class UsuariosConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'usuarios'

    def ready(self):
        # Importa o signals.py para registrar os receptores de login/logout
        # (item 5.1). O import so acontece aqui, e nao lá em cima do arquivo,
        # porque o Django ainda nao terminou de carregar todos os apps quando
        # este arquivo e lido pela primeira vez.
        import usuarios.signals  # noqa: F401