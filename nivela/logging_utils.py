"""
Utilitarios de log do projeto Nivela (item 5.3 do Requisito 5 - protecao
contra alteracao dos logs).

Estrategia de protecao usada:
1) O arquivo e sempre aberto em modo "append" (padrao do FileHandler do
   Python), nunca sobrescrevendo o conteudo ja gravado.
2) Em producao (Render/Linux), a pasta 'logs/' recebe permissao
   restrita (configurado em settings.py), impedindo outros usuarios do
   sistema de ler ou alterar os arquivos.
3) Cada linha do log carrega um hash SHA-256 encadeado com o hash da
   linha anterior (como uma mini blockchain). Se alguem editar, apagar
   ou inserir uma linha no meio do arquivo depois de gravada, a cadeia
   de hashes deixa de bater a partir daquele ponto - o que e detectado
   rodando o comando `python manage.py verificar_logs <arquivo>`.
"""
import hashlib
import logging
import os


class FileHandlerComHashEncadeado(logging.FileHandler):
    """FileHandler que grava um hash SHA-256 encadeado ao final de cada linha."""

    # Hash "semente", usado como ponto de partida da cadeia quando o
    # arquivo de log ainda nao existe ou esta vazio.
    HASH_SEMENTE = '0' * 64

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Ao abrir o arquivo (inclusive apos reiniciar o servidor),
        # retoma a cadeia a partir do hash da ultima linha ja gravada,
        # entao a protecao continua valendo entre reinicios.
        self._hash_anterior = self._ler_ultimo_hash()

    def _ler_ultimo_hash(self):
        if not os.path.exists(self.baseFilename):
            return self.HASH_SEMENTE
        try:
            with open(self.baseFilename, 'r', encoding='utf-8') as arquivo:
                linhas = [linha for linha in arquivo if linha.strip()]
        except OSError:
            return self.HASH_SEMENTE

        if not linhas:
            return self.HASH_SEMENTE

        ultima_linha = linhas[-1]
        if '| hash=' in ultima_linha:
            return ultima_linha.rsplit('| hash=', 1)[1].strip()
        return self.HASH_SEMENTE

    def emit(self, record):
        try:
            mensagem = self.format(record)
            hash_atual = hashlib.sha256(
                (self._hash_anterior + mensagem).encode('utf-8')
            ).hexdigest()
            self._hash_anterior = hash_atual

            linha_final = f'{mensagem} | hash={hash_atual}'
            self.stream.write(linha_final + self.terminator)
            self.flush()
        except Exception:
            self.handleError(record)