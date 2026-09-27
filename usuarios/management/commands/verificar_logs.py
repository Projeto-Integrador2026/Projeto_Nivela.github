"""
Verifica a integridade da cadeia de hashes de um arquivo de log (item 5.3).

Recalcula o hash de cada linha, na ordem em que aparecem no arquivo, e
compara com o hash gravado nela. Se alguma linha foi editada, apagada ou
inserida no meio do arquivo depois de gravada, a cadeia deixa de bater a
partir daquele ponto, e o comando aponta exatamente onde.

Uso:
    python manage.py verificar_logs logs/autenticacao.log
    python manage.py verificar_logs logs/recuperacao_senha.log
"""
import hashlib

from django.core.management.base import BaseCommand, CommandError

from nivela.logging_utils import FileHandlerComHashEncadeado


class Command(BaseCommand):
    help = 'Verifica se a cadeia de hashes de um arquivo de log foi alterada.'

    def add_arguments(self, parser):
        parser.add_argument('caminho', type=str, help='Caminho do arquivo de log a verificar.')

    def handle(self, *args, **opcoes):
        caminho = opcoes['caminho']

        try:
            with open(caminho, 'r', encoding='utf-8') as arquivo:
                linhas = [linha.rstrip('\n') for linha in arquivo if linha.strip()]
        except OSError as erro:
            raise CommandError(f'Não foi possível abrir o arquivo: {erro}')

        if not linhas:
            self.stdout.write(self.style.WARNING('Arquivo vazio - nada para verificar.'))
            return

        hash_anterior = FileHandlerComHashEncadeado.HASH_SEMENTE
        for numero, linha in enumerate(linhas, start=1):
            if '| hash=' not in linha:
                raise CommandError(
                    f'Linha {numero} não tem o formato esperado (sem "| hash="): {linha}'
                )

            conteudo, hash_gravado = linha.rsplit('| hash=', 1)
            conteudo = conteudo.rstrip()
            hash_gravado = hash_gravado.strip()

            hash_esperado = hashlib.sha256(
                (hash_anterior + conteudo).encode('utf-8')
            ).hexdigest()

            if hash_esperado != hash_gravado:
                self.stdout.write(self.style.ERROR(
                    f'ADULTERAÇÃO DETECTADA na linha {numero}:'
                ))
                self.stdout.write(f'  Conteúdo: {conteudo}')
                self.stdout.write(f'  Hash esperado : {hash_esperado}')
                self.stdout.write(f'  Hash encontrado: {hash_gravado}')
                return

            hash_anterior = hash_gravado

        self.stdout.write(self.style.SUCCESS(
            f'OK - {len(linhas)} linha(s) verificada(s), nenhuma adulteração detectada.'
        ))