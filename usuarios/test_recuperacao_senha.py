"""Testes da recuperação de senha (itens 2.2 a 2.7 do checklist)."""
from unittest import mock

from django.contrib.auth import get_user_model
from django.contrib.auth.tokens import default_token_generator
from django.core import mail
from django.test import Client, TestCase, override_settings
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode

SENHA_ANTIGA = "SenhaAntiga#2026"
SENHA_NOVA = "NovaSenhaForte#2026"
LOGGER = "usuarios.recuperacao_senha"


# O teste roda com DEBUG=False; estas opções evitam depender do collectstatic
# e do redirecionamento para HTTPS (mesmo padrão dos outros testes do projeto)
@override_settings(
    SECURE_SSL_REDIRECT=False,
    STORAGES={
        "default": {"BACKEND": "django.core.files.storage.FileSystemStorage"},
        "staticfiles": {"BACKEND": "django.contrib.staticfiles.storage.StaticFilesStorage"},
    },
)
class RecuperacaoSenhaTests(TestCase):

    def setUp(self):
        self.usuario = get_user_model().objects.create_user(
            username="maria@example.com",
            email="maria@example.com",
            password=SENHA_ANTIGA,
        )

    def _link(self, usuario=None):
        """Monta o link de recuperação, igual ao que vai no e-mail."""
        usuario = usuario or self.usuario
        uid = urlsafe_base64_encode(force_bytes(usuario.pk))
        token = default_token_generator.make_token(usuario)
        return f"/recuperar-senha/confirmar/{uid}/{token}/"

    def _abrir_link(self, cliente, link):
        """Abre o link; o Django troca o token por um endereço 'set-password'."""
        resposta = cliente.get(link, follow=True)
        return resposta, resposta.redirect_chain[-1][0] if resposta.redirect_chain else link

    # --- 2.1 / achado de enumeração -------------------------------------

    def test_resposta_igual_para_email_existente_e_inexistente(self):
        r1 = Client().post("/recuperar-senha/", {"email": "maria@example.com"})
        r2 = Client().post("/recuperar-senha/", {"email": "naoexiste@example.com"})
        self.assertEqual(r1.status_code, r2.status_code)
        self.assertEqual(r1.url, r2.url)
        # só o e-mail cadastrado recebe a mensagem
        self.assertEqual(len(mail.outbox), 1)
        self.assertEqual(mail.outbox[0].to, ["maria@example.com"])

    def test_falha_no_envio_do_email_nao_gera_erro_500(self):
        with mock.patch(
            "django.core.mail.backends.locmem.EmailBackend.send_messages",
            side_effect=OSError("smtp bloqueado"),
        ) as envio:
            resposta = Client().post("/recuperar-senha/", {"email": "maria@example.com"})
        # o envio foi tentado e falhou, mas o usuario recebe a resposta normal
        self.assertTrue(envio.called)
        self.assertRedirects(resposta, "/recuperar-senha/enviado/", fetch_redirect_response=False)

    # --- 2.6 ------------------------------------------------------------

    def test_solicitacao_e_registrada_com_email_mascarado_e_ip(self):
        with self.assertLogs(LOGGER, level="INFO") as captura:
            Client().post("/recuperar-senha/", {"email": "maria@example.com"})
        texto = " ".join(captura.output)
        self.assertIn("m***@example.com", texto)
        self.assertNotIn("maria@example.com", texto)
        self.assertIn("IP:", texto)

    # --- 2.2 / 2.4 ------------------------------------------------------

    def test_link_valido_abre_o_formulario_de_nova_senha(self):
        resposta, _ = self._abrir_link(Client(), self._link())
        self.assertEqual(resposta.status_code, 200)
        self.assertTrue(resposta.context["validlink"])

    def test_link_so_funciona_uma_vez_e_nao_faz_login_automatico(self):
        link = self._link()
        cliente = Client()
        _, url_formulario = self._abrir_link(cliente, link)

        with self.assertLogs(LOGGER, level="INFO") as captura:
            resposta = cliente.post(url_formulario, {
                "new_password1": SENHA_NOVA,
                "new_password2": SENHA_NOVA,
            })
        self.assertRedirects(resposta, "/recuperar-senha/concluido/", fetch_redirect_response=False)
        self.assertIn("SUCESSO", " ".join(captura.output))

        self.usuario.refresh_from_db()
        self.assertTrue(self.usuario.check_password(SENHA_NOVA))
        # a redefinição não pode pular o 2FA: o usuário continua sem sessão
        self.assertNotIn("_auth_user_id", cliente.session)

        # reutilizar o mesmo link (item 2.4)
        resposta, _ = self._abrir_link(Client(), link)
        self.assertFalse(resposta.context["validlink"])

    # --- 2.3 / 2.5 ------------------------------------------------------

    def test_link_expirado_mostra_link_invalido(self):
        link = self._link()
        # Timeout negativo: qualquer token, mesmo recém-criado, já nasce vencido
        with override_settings(PASSWORD_RESET_TIMEOUT=-1):
            resposta, _ = self._abrir_link(Client(), link)
        self.assertEqual(resposta.status_code, 200)
        self.assertFalse(resposta.context["validlink"])
        self.assertContains(resposta, "Link inválido")

    def test_timeout_configurado_e_de_uma_hora(self):
        from django.conf import settings
        self.assertEqual(settings.PASSWORD_RESET_TIMEOUT, 3600)

    # --- 2.7 ------------------------------------------------------------

    def test_link_invalido_e_registrado_no_log(self):
        with self.assertLogs(LOGGER, level="WARNING") as captura:
            resposta = Client().get("/recuperar-senha/confirmar/xx/token-invalido/", follow=True)
        self.assertFalse(resposta.context["validlink"])
        texto = " ".join(captura.output)
        self.assertIn("link invalido", texto)
        self.assertIn("IP:", texto)

    def test_senha_fraca_e_rejeitada_e_registrada_no_log(self):
        cliente = Client()
        _, url_formulario = self._abrir_link(cliente, self._link())

        with self.assertLogs(LOGGER, level="WARNING") as captura:
            resposta = cliente.post(url_formulario, {
                "new_password1": "12345678",
                "new_password2": "12345678",
            })
        self.assertEqual(resposta.status_code, 200)  # reexibe o formulário
        self.assertIn("FALHA ao redefinir senha", " ".join(captura.output))
        self.usuario.refresh_from_db()
        self.assertTrue(self.usuario.check_password(SENHA_ANTIGA))