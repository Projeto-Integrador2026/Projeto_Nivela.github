from axes.models import AccessAttempt, AccessLog
from django.contrib.auth import get_user_model
from django.test import Client, TestCase, override_settings

SENHA_CERTA = "SenhaCorreta#2026"

# O teste roda com DEBUG=False; estas opções evitam depender do collectstatic
# e do redirecionamento para HTTPS, que só valem em produção.
@override_settings(
    SECURE_SSL_REDIRECT=False,
    STORAGES={
        "default": {"BACKEND": "django.core.files.storage.FileSystemStorage"},
        "staticfiles": {"BACKEND": "django.contrib.staticfiles.storage.StaticFilesStorage"},
    },
)
class AxesPrivacidadeTests(TestCase):
    """Garante que o django-axes não guarda senha e bloqueia por conta."""

    def setUp(self):
        User = get_user_model()
        for email in ("a@example.com", "b@example.com"):
            User.objects.create_user(username=email, email=email, password=SENHA_CERTA)

    def _login(self, email, senha, ip="10.0.0.1"):
        return Client(REMOTE_ADDR=ip).post("/account/login/", {
            "login_view-current_step": "auth",
            "auth-username": email,
            "auth-password": senha,
        })

    def test_falha_nao_grava_senha_nem_email_em_texto_puro(self):
        self._login("a@example.com", "SenhaErrada#123")
        tentativa = AccessAttempt.objects.get()
        self.assertNotIn("SenhaErrada#123", tentativa.post_data)
        self.assertNotIn("a@example.com", tentativa.post_data)
        # o e-mail fica só na coluna própria, que a exclusão de dados consegue achar
        self.assertEqual(tentativa.username, "a@example.com")

    def test_bloqueio_vale_por_conta_mesmo_trocando_de_ip(self):
        for _ in range(5):
            self._login("a@example.com", "errada", ip="10.0.0.1")
        resposta = self._login("a@example.com", SENHA_CERTA, ip="10.0.0.2")
        self.assertEqual(resposta.status_code, 429)

    def test_login_bem_sucedido_registra_o_email_no_accesslog(self):
        self._login("b@example.com", SENHA_CERTA)
        self.assertEqual(AccessLog.objects.get().username, "b@example.com")