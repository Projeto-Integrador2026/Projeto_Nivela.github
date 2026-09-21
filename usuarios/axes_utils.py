"""Funções de apoio para o django-axes (proteção contra força bruta)."""


def obter_username_login(request, credentials):
    """Informa ao axes qual e-mail está tentando entrar.

    Por padrão o axes procura o e-mail em um campo chamado "email", mas o
    login com 2FA (django-two-factor-auth) envia o campo "auth-username".
    Sem esta função o axes gravava o usuário como vazio, o que:
      - fazia o bloqueio valer só por IP e não por conta;
      - misturava, numa mesma linha do banco, as tentativas de pessoas
        diferentes que usavam o mesmo IP.
    """
    if credentials:
        # "username" vem do login normal; "email" vem de chamadas internas do axes
        valor = credentials.get('username') or credentials.get('email')
        if valor:
            return valor
    # Sem credentials (ex.: passo do código 2FA): lê o campo do formulário
    dados = getattr(request, 'POST', None)
    if dados is not None:
        return dados.get('auth-username')
    return None