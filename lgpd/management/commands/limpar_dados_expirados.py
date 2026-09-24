"""Descarte de dados pessoais vencidos (política de retenção, LGPD art. 15 e 16).

Prazos definidos pelo grupo:
  - registros de acesso do django-axes (logins e tentativas): 6 meses (180 dias);
  - sessões já expiradas: 30 dias depois de expirar.

Uso:
    python manage.py limpar_dados_expirados --simular   (só mostra, não apaga)
    python manage.py limpar_dados_expirados             (apaga de verdade)
"""
from datetime import timedelta

from axes.models import AccessAttempt, AccessFailureLog, AccessLog
from django.contrib.sessions.models import Session
from django.core.management.base import BaseCommand, CommandError
from django.utils import timezone

DIAS_REGISTROS_ACESSO = 180
DIAS_SESSAO_EXPIRADA = 30


class Command(BaseCommand):
    help = 'Apaga registros de acesso e sessões que passaram do prazo de retenção.'

    def add_arguments(self, parser):
        parser.add_argument('--dias-acesso', type=int, default=DIAS_REGISTROS_ACESSO,
                            help='Prazo dos registros do axes, em dias (padrão: 180).')
        parser.add_argument('--dias-sessao', type=int, default=DIAS_SESSAO_EXPIRADA,
                            help='Dias depois de expirada até apagar a sessão (padrão: 30).')
        parser.add_argument('--simular', action='store_true',
                            help='Só mostra quantos registros seriam apagados.')

    def handle(self, *args, **opcoes):
        if opcoes['dias_acesso'] < 0 or opcoes['dias_sessao'] < 0:
            raise CommandError('Os prazos não podem ser negativos.')

        agora = timezone.now()
        limite_acesso = agora - timedelta(days=opcoes['dias_acesso'])
        limite_sessao = agora - timedelta(days=opcoes['dias_sessao'])

        alvos = [
            ('Logins bem-sucedidos (axes_accesslog)',
             AccessLog.objects.filter(attempt_time__lt=limite_acesso)),
            ('Tentativas de login falhas (axes_accessattempt)',
             AccessAttempt.objects.filter(attempt_time__lt=limite_acesso)),
            ('Falhas registradas (axes_accessfailurelog)',
             AccessFailureLog.objects.filter(attempt_time__lt=limite_acesso)),
            ('Sessões expiradas (django_session)',
             Session.objects.filter(expire_date__lt=limite_sessao)),
        ]

        modo = 'SIMULAÇÃO (nada foi apagado)' if opcoes['simular'] else 'APAGADOS'
        self.stdout.write(f'Retenção - {modo}:')
        for nome, consulta in alvos:
            quantidade = consulta.count()
            if not opcoes['simular']:
                consulta.delete()
            self.stdout.write(f'  {nome}: {quantidade}')