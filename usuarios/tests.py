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


@override_settings(
    SECURE_SSL_REDIRECT=False,
    STORAGES={
        "default": {"BACKEND": "django.core.files.storage.FileSystemStorage"},
        "staticfiles": {"BACKEND": "django.contrib.staticfiles.storage.StaticFilesStorage"},
    },
)
class LoginGlobalTests(TestCase):
    """Garante que o site inteiro exige login, exceto as rotas publicas."""

    ROTAS_PROTEGIDAS = ["/", "/turmas/", "/nivelamento/", "/meus-dados/"]
    ROTAS_PUBLICAS = ["/cadastro/", "/recuperar-senha/", "/account/login/"]

    def test_visitante_anonimo_vai_para_o_login(self):
        for caminho in self.ROTAS_PROTEGIDAS:
            with self.subTest(caminho=caminho):
                resposta = self.client.get(caminho)
                self.assertRedirects(
                    resposta,
                    f"/account/login/?next={caminho}",
                    fetch_redirect_response=False,
                )

    def test_rotas_publicas_abrem_sem_login(self):
        for caminho in self.ROTAS_PUBLICAS:
            with self.subTest(caminho=caminho):
                self.assertEqual(self.client.get(caminho).status_code, 200)

    def test_favicon_nao_e_redirecionado_para_o_login(self):
        # Se o favicon fosse redirecionado, o navegador reiniciaria o
        # assistente de login do 2FA no meio do caminho (bug ja visto).
        resposta = self.client.get("/favicon.ico")
        self.assertEqual(resposta.status_code, 404)

    def test_logado_sem_2fa_consegue_sair(self):
        usuario = get_user_model().objects.create_user(
            username="sem2fa@example.com",
            email="sem2fa@example.com",
            password=SENHA_CERTA,
        )
        self.client.force_login(usuario)
        resposta = self.client.post("/sair/")
        # Deve ir para o login, e nao ser preso na tela de configurar o 2FA
        self.assertRedirects(resposta, "/account/login/", fetch_redirect_response=False)

    def test_logado_sem_2fa_e_levado_para_configurar_o_2fa(self):
        usuario = get_user_model().objects.create_user(
            username="sem2fa@example.com",
            email="sem2fa@example.com",
            password=SENHA_CERTA,
        )
        self.client.force_login(usuario)
        resposta = self.client.get("/turmas/")
        self.assertRedirects(
            resposta, "/account/two_factor/setup/", fetch_redirect_response=False
        )