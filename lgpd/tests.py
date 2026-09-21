import logging
from datetime import timedelta
from io import StringIO

from axes.models import AccessAttempt, AccessLog
from django.contrib.sessions.models import Session
from django.core.management import call_command
from django.test import TestCase, override_settings
from django.utils import timezone

from lgpd.utils import mascarar_email


class MascararEmailTests(TestCase):
    def test_mostra_so_a_primeira_letra_e_o_dominio(self):
        self.assertEqual(mascarar_email('maria.silva@gmail.com'), 'm***@gmail.com')

    def test_valor_vazio_ou_invalido_nao_quebra(self):
        self.assertEqual(mascarar_email(None), '***')
        self.assertEqual(mascarar_email('sem-arroba'), '***')


@override_settings(SECURE_SSL_REDIRECT=False)
class LogRecuperacaoSenhaTests(TestCase):
    def test_log_nao_guarda_o_email_completo(self):
        with self.assertLogs('usuarios.recuperacao_senha', level='INFO') as captura:
            self.client.post('/recuperar-senha/', {'email': 'maria.silva@example.com'})
        texto = ' '.join(captura.output)
        self.assertIn('m***@example.com', texto)
        self.assertNotIn('maria.silva', texto)

    def test_log_grava_data_e_hora(self):
        manipulador = logging.getLogger('usuarios.recuperacao_senha').handlers[0]
        self.assertIn('asctime', manipulador.formatter._fmt)


class LimparDadosExpiradosTests(TestCase):
    def _log_com_idade(self, dias):
        registro = AccessLog.objects.create(
            username='a@example.com', ip_address='10.0.0.1', user_agent='ua',
            http_accept='x', path_info='/')
        AccessLog.objects.filter(pk=registro.pk).update(
            attempt_time=timezone.now() - timedelta(days=dias))

    def _executar(self, *argumentos):
        saida = StringIO()
        call_command('limpar_dados_expirados', *argumentos, stdout=saida)
        return saida.getvalue()

    def test_apaga_acessos_com_mais_de_6_meses_e_mantem_os_recentes(self):
        self._log_com_idade(200)
        self._log_com_idade(10)
        self._executar()
        self.assertEqual(AccessLog.objects.count(), 1)

    def test_simular_nao_apaga_nada(self):
        self._log_com_idade(200)
        texto = self._executar('--simular')
        self.assertEqual(AccessLog.objects.count(), 1)
        self.assertIn('SIMULAÇÃO', texto)

    def test_apaga_tentativas_falhas_antigas(self):
        antiga = AccessAttempt.objects.create(
            ip_address='10.0.0.1', user_agent='ua', http_accept='x', path_info='/',
            get_data='', post_data='', failures_since_start=1)
        AccessAttempt.objects.filter(pk=antiga.pk).update(
            attempt_time=timezone.now() - timedelta(days=200))
        self._executar()
        self.assertEqual(AccessAttempt.objects.count(), 0)

    def test_sessao_expirada_ha_mais_de_30_dias_e_apagada(self):
        agora = timezone.now()
        Session.objects.create(session_key='velha', session_data='x',
                               expire_date=agora - timedelta(days=31))
        Session.objects.create(session_key='recente', session_data='x',
                               expire_date=agora - timedelta(days=5))
        Session.objects.create(session_key='ativa', session_data='x',
                               expire_date=agora + timedelta(minutes=20))
        self._executar()
        self.assertEqual(sorted(Session.objects.values_list('session_key', flat=True)),
                         ['ativa', 'recente'])