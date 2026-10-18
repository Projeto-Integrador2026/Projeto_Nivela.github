"""Testes dos fluxos de cadastro (conta ativa, sem e-mail de ativacao) e direitos do titular (LGPD)."""
 
from axes.models import AccessAttempt
from django.contrib.auth import get_user_model
from django.core import mail
from django.test import TestCase, override_settings
from django_otp.plugins.otp_totp.models import TOTPDevice
 
from lgpd.models import SolicitacaoTitular
 
SENHA = "SenhaForte#2026x"
 
CONFIG = dict(
    SECURE_SSL_REDIRECT=False,
    EMAIL_BACKEND="django.core.mail.backends.locmem.EmailBackend",
    STORAGES={
        "default": {"BACKEND": "django.core.files.storage.FileSystemStorage"},
        "staticfiles": {"BACKEND": "django.contrib.staticfiles.storage.StaticFilesStorage"},
    },
)
 
 
@override_settings(**CONFIG)
class CadastroTests(TestCase):
    def _cadastrar(self, email, senha=SENHA, termos=True):
        dados = {"email": email, "password1": senha, "password2": senha}
        if termos:
            dados["aceite_termos"] = "on"
        return self.client.post("/cadastro/", dados)
 
    def test_paginas_legais_sao_publicas_com_ou_sem_barra(self):
        for caminho in ("/termos/", "/privacidade/", "/termos", "/privacidade"):
            with self.subTest(caminho=caminho):
                self.assertEqual(self.client.get(caminho, follow=True).status_code, 200)
 
    def test_cadastro_cria_conta_ativa_sem_enviar_email(self):
        resposta = self._cadastrar("novo@example.com")
        self.assertRedirects(resposta, "/account/login/", fetch_redirect_response=False)
        usuario = get_user_model().objects.get(email="novo@example.com")
        self.assertTrue(usuario.is_active)
        self.assertEqual(len(mail.outbox), 0)
 
    def test_conta_nova_consegue_entrar(self):
        self._cadastrar("novo@example.com")
        self.client.post("/account/login/", {
            "login_view-current_step": "auth",
            "auth-username": "novo@example.com",
            "auth-password": SENHA,
        })
        self.assertIn("_auth_user_id", self.client.session)
 
    def test_email_repetido_responde_igual_e_nao_cria_conta(self):
        get_user_model().objects.create_user(username="a@example.com", email="a@example.com", password=SENHA)
        for variante in ("a@example.com", "A@Example.com"):
            with self.subTest(email=variante):
                resposta = self._cadastrar(variante)
                self.assertRedirects(resposta, "/account/login/", fetch_redirect_response=False)
        self.assertEqual(get_user_model().objects.count(), 1)
        self.assertEqual(len(mail.outbox), 0)  # o cadastro nao envia e-mail
 
    def test_email_repetido_com_senha_fraca_mostra_so_o_erro_da_senha(self):
        get_user_model().objects.create_user(username="a@example.com", email="a@example.com", password=SENHA)
        resposta = self._cadastrar("a@example.com", senha="123")
        self.assertEqual(resposta.status_code, 200)
        self.assertNotIn("já existe", resposta.content.decode().lower())
 
 
@override_settings(**CONFIG)
class DireitosDoTitularTests(TestCase):
    def setUp(self):
        self.usuario = get_user_model().objects.create_user(
            username="b@example.com", email="b@example.com", password=SENHA)
        TOTPDevice.objects.create(user=self.usuario, name="d", confirmed=True)
        self.client.force_login(self.usuario)
 
    def test_meus_dados_registra_solicitacao_de_acesso(self):
        self.assertEqual(self.client.get("/meus-dados/").status_code, 200)
        self.assertTrue(SolicitacaoTitular.objects.filter(tipo="acesso", usuario=self.usuario).exists())
 
    def test_exportar_registra_solicitacao_de_exportacao(self):
        self.assertEqual(self.client.get("/meus-dados/exportar/").status_code, 200)
        self.assertTrue(SolicitacaoTitular.objects.filter(tipo="exportacao", usuario=self.usuario).exists())
 
    def test_revogar_registra_solicitacao_de_revogacao(self):
        from lgpd.models import RegistroConsentimento
        c = RegistroConsentimento.objects.create(
            usuario=self.usuario, finalidade="termos_uso", versao_termo="1.0")
        self.client.post(f"/meus-dados/consentimentos/{c.pk}/revogar/")
        self.assertTrue(SolicitacaoTitular.objects.filter(tipo="revogacao").exists())
 
    def test_excluir_conta_apaga_usuario_e_rastros_do_axes(self):
        AccessAttempt.objects.create(
            username="b@example.com", ip_address="10.0.0.1", user_agent="ua",
            http_accept="x", path_info="/", get_data="", post_data="", failures_since_start=1)
        self.client.post("/meus-dados/excluir/", {"senha": SENHA, "confirmar": "on"})
        self.assertFalse(get_user_model().objects.filter(email="b@example.com").exists())
        self.assertEqual(AccessAttempt.objects.filter(username="b@example.com").count(), 0)
        # o protocolo anonimo sobrevive a exclusao
        self.assertTrue(SolicitacaoTitular.objects.filter(tipo="exclusao", usuario=None).exists())
 