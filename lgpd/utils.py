"""Funções de apoio do módulo LGPD."""


def mascarar_email(email):
    """Esconde a maior parte do e-mail para uso em logs (minimização, item 4.3).

    Exemplo: 'maria.silva@gmail.com' -> 'm***@gmail.com'.
    """
    if not email or '@' not in email:
        return '***'
    usuario, dominio = email.split('@', 1)
    return f'{usuario[:1]}***@{dominio}'