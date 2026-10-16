"""Funções de apoio do módulo LGPD."""


def mascarar_email(email):
    """Esconde a maior parte do e-mail para uso em logs (minimização, item 4.3).

    Exemplo: 'maria.silva@gmail.com' -> 'm***@gmail.com'.
    """
    if not email or '@' not in email:
        return '***'
    usuario, dominio = email.split('@', 1)
    return f'{usuario[:1]}***@{dominio}'


"""Funções de apoio do módulo LGPD."""


def sanitizar_log(valor):
    """Remove quebras de linha para impedir injeção em logs (CWE-117)."""
    if valor is None:
        return ''
    return str(valor).replace('\r', '').replace('\n', '')


def mascarar_email(email):
    """Esconde a maior parte do e-mail para uso em logs (minimização, item 4.3).

    Exemplo: 'maria.silva@gmail.com' -> 'm***@gmail.com'.
    """
    email = sanitizar_log(email)
    if not email or '@' not in email:
        return '***'
    usuario, dominio = email.split('@', 1)
    return f'{usuario[:1]}***@{dominio}'