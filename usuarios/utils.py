"""Funções de apoio para o log de autenticação (item 5.1)."""


def obter_ip_cliente(request):
    """Descobre o IP de quem está fazendo a requisição.

    Em produção (Render), a aplicação fica atras de um proxy reverso,
    entao o IP real de quem acessa vem no cabecalho HTTP_X_FORWARDED_FOR,
    e nao em REQUEST.META['REMOTE_ADDR'] (que traria o IP do proprio
    proxy). Localmente esse cabecalho nao existe, entao cai no
    REMOTE_ADDR normal.
    """
    if request is None:
        return None

    encaminhado_por = request.META.get('HTTP_X_FORWARDED_FOR')
    if encaminhado_por:
        # O cabecalho pode conter uma lista "cliente, proxy1, proxy2..."
        # separada por virgula; o primeiro IP e o do cliente original.
        return encaminhado_por.split(',')[0].strip()

    return request.META.get('REMOTE_ADDR')