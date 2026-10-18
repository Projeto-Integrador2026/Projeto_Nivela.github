"""
Hasher de senhas customizado do Nivela (item 1.2 do checklist).

O Django ja usa PBKDF2-SHA256 com 1.000.000 de iteracoes por padrao (versao 5.2),
mas esse numero vem do framework e pode mudar numa atualizacao. Aqui o custo fica
fixado em codigo, entao so muda quando a equipe decidir.

O nome do algoritmo continua 'pbkdf2_sha256', por isso as senhas ja gravadas
no banco continuam validas. Se o custo for alterado no futuro, o Django
atualiza o hash automaticamente no proximo login de cada usuario.
"""
from django.contrib.auth.hashers import PBKDF2PasswordHasher


class PBKDF2Nivela(PBKDF2PasswordHasher):
    """PBKDF2-SHA256 com numero de iteracoes definido explicitamente."""

    iterations = 1_000_000