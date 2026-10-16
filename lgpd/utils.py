"""
Módulo de Utilitários e Funções de Apoio para LGPD e Segurança.

Este arquivo reúne funções auxiliares para sanitização de entradas
em arquivos de log (prevenção de CWE-117 / Injeção em Log) e
mascaramento de dados pessoais (minimização de dados exigida pelo Art. 6º da LGPD).
"""


def sanitizar_log(texto: str) -> str:
    """
    Sanitiza uma string removendo quebras de linha e caracteres de controle.

    Previne vulnerabilidades de Injeção em Log (CWE-117 / Achado A-09), garantindo
    que um atacante não consiga forjar registros falsos nos arquivos de auditoria.

    Args:
        texto (str): O texto ou identificador a ser gravado no log.

    Returns:
        str: Texto sanitizado com quebras de linha substituídas por sublinhado.
    """
    if not texto:
        return ''
    
    # Substitui caracteres de quebra de linha por sublinhado e remove espaços nas pontas
    return str(texto).replace('\r', '_').replace('\n', '_').strip()


def mascarar_email(email: str) -> str:
    """
    Aplica o princípio de minimização de dados da LGPD (Art. 6º, III) sobre e-mails.

    Sanitiza o e-mail contra injeção de log e substitui os caracteres intermediários
    do nome de usuário por asteriscos (ex.: 'beatriz@dominio.com' -> 'b*****z@dominio.com').

    Args:
        email (str): O endereço de e-mail original a ser mascarado.

    Returns:
        str: E-mail mascarado seguro para exibição em registros de auditoria ou 'email_invalido'.
    """
    email = sanitizar_log(email)
    
    if not email or '@' not in email:
        return 'email_invalido'

    nome, dominio = email.split('@', 1)

    # Tratamento para nomes curtos (1 ou 2 caracteres, ex.: 'a@dom.com' -> 'a*@dom.com')
    if len(nome) <= 2:
        nome_mascarado = nome[0] + '*'
    else:
        # Preserva a primeira e a última letra do usuário, mascarando o meio
        nome_mascarado = nome[0] + '*' * (len(nome) - 2) + nome[-1]

    return f"{nome_mascarado}@{dominio}"