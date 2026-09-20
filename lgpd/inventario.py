"""Inventário dos dados pessoais tratados pelo Nivela.

Atende aos itens 4.1 (listagem dos dados), 4.2 (finalidade de cada dado)
e 4.3 (minimização) do checklist de LGPD. A página "Meus dados" e a
exportação (Fases 5 e 6) usarão esta lista.
"""

# Versão atual dos Termos de Uso / Política de Privacidade.
# Sempre que o texto mudar, aumente esta versão (ex.: "1.1"), pois ela é
# gravada em cada consentimento (item 4.7).
VERSAO_TERMOS = "1.0"

# Bases legais (Lei nº 13.709/2018, art. 7º)
CONSENTIMENTO = "Consentimento (art. 7º, I)"
OBRIGACAO_LEGAL = "Cumprimento de obrigação legal (art. 7º, II)"
CONTRATO = "Execução de contrato (art. 7º, V)"
LEGITIMO_INTERESSE = "Legítimo interesse (art. 7º, IX)"

DADOS_PESSOAIS = [
    {
        "dado": "E-mail",
        "origem": "Informado pelo titular no cadastro",
        "armazenamento": "usuarios_usuario.email",
        "finalidade": "Identificar o titular, autenticar o login (RF02) e enviar o link de recuperação de senha",
        "base_legal": CONTRATO,
        "obrigatorio": True,
        "protecao": "Transmissão por HTTPS; acesso restrito ao banco",
        "retencao": "Enquanto a conta existir",
    },
    {
        "dado": "Senha",
        "origem": "Informada pelo titular no cadastro",
        "armazenamento": "usuarios_usuario.password (somente o hash)",
        "finalidade": "Autenticar o titular",
        "base_legal": CONTRATO,
        "obrigatorio": True,
        "protecao": "Hash PBKDF2-SHA256 com salt único; nunca guardada em texto puro",
        "retencao": "Enquanto a conta existir",
    },
    {
        "dado": "Nome de usuário (username)",
        "origem": "Preenchido automaticamente com o e-mail",
        "armazenamento": "usuarios_usuario.username",
        "finalidade": "Exigência técnica do modelo de usuário do Django (não é usado no login)",
        "base_legal": CONTRATO,
        "obrigatorio": True,
        "protecao": "Acesso restrito ao banco",
        "retencao": "Enquanto a conta existir",
    },
    {
        "dado": "Telefone",
        "origem": "Informado pelo titular (campo opcional)",
        "armazenamento": "usuarios_usuario.telefone",
        "finalidade": "Contato com o titular (opcional)",
        "base_legal": CONSENTIMENTO,
        "obrigatorio": False,
        "protecao": "Criptografado em repouso com Fernet (AES-128-CBC + HMAC-SHA256); chave separada da SECRET_KEY",
        "retencao": "Até a revogação do consentimento ou a exclusão da conta",
    },
    {
        "dado": "Datas de criação e de último acesso da conta",
        "origem": "Geradas pelo sistema",
        "armazenamento": "usuarios_usuario.date_joined e last_login",
        "finalidade": "Controle e segurança da conta",
        "base_legal": LEGITIMO_INTERESSE,
        "obrigatorio": True,
        "protecao": "Acesso restrito ao banco",
        "retencao": "Enquanto a conta existir",
    },
    {
        "dado": "Dados do 2FA (chave do autenticador e códigos de backup)",
        "origem": "Gerados quando o titular ativa a verificação em duas etapas",
        "armazenamento": "Tabelas do django-otp",
        "finalidade": "Verificação em duas etapas no login (item 1.5)",
        "base_legal": LEGITIMO_INTERESSE,
        "obrigatorio": False,
        "protecao": "Acesso restrito ao banco",
        "retencao": "Até o titular desativar o 2FA ou excluir a conta",
    },
    {
        "dado": "Sessão e cookies técnicos",
        "origem": "Gerados no login",
        "armazenamento": "Tabela django_session; cookies sessionid e csrftoken",
        "finalidade": "Manter o titular autenticado e proteger os formulários (CSRF)",
        "base_legal": CONTRATO,
        "obrigatorio": True,
        "protecao": "Cookie de sessão com HttpOnly e Secure; sessão com expiração",
        "retencao": "Até a expiração da sessão",
    },
    {
        "dado": "Tentativas de login (usuário informado, IP, navegador e data)",
        "origem": "Geradas pelo sistema a cada tentativa de login",
        "armazenamento": "Tabelas do django-axes",
        "finalidade": "Proteção contra força bruta (item 1.11)",
        "base_legal": LEGITIMO_INTERESSE,
        "obrigatorio": True,
        "protecao": "Acesso restrito ao banco",
        "retencao": "A definir pelo grupo (prazo de descarte)",
    },
    {
        "dado": "Log de recuperação de senha (e-mail informado e data)",
        "origem": "Gerado pelo sistema a cada pedido de recuperação",
        "armazenamento": "Arquivo logs/recuperacao_senha.log",
        "finalidade": "Auditoria do fluxo de recuperação de senha (itens 2.6 e 2.7)",
        "base_legal": LEGITIMO_INTERESSE,
        "obrigatorio": True,
        "protecao": "Arquivo fora do repositório (.gitignore)",
        "retencao": "Enquanto o arquivo existir (no plano gratuito do Render o disco é apagado a cada deploy)",
    },
    {
        "dado": "Registros de acesso da hospedagem (IP, URL e navegador)",
        "origem": "Gerados pela infraestrutura (Render e Cloudflare)",
        "armazenamento": "Infraestrutura de terceiros (operadores)",
        "finalidade": "Operação e segurança da hospedagem",
        "base_legal": LEGITIMO_INTERESSE,
        "obrigatorio": True,
        "protecao": "Gerenciada pelos provedores",
        "retencao": "Conforme a política de cada provedor",
    },
    {
        "dado": "Registros de consentimento e de solicitações do titular",
        "origem": "Gerados pelo módulo LGPD do Nivela",
        "armazenamento": "lgpd_registroconsentimento e lgpd_solicitacaotitular",
        "finalidade": "Comprovar o consentimento e o atendimento dos direitos do titular",
        "base_legal": OBRIGACAO_LEGAL,
        "obrigatorio": True,
        "protecao": "Acesso restrito ao banco; após a exclusão, as solicitações guardam só um identificador anônimo",
        "retencao": "Consentimentos: apagados com a conta. Solicitações: mantidas sem dados pessoais",
    },
]

# Dados que o sistema NÃO coleta (evidência de minimização, item 4.3)
CAMPOS_NAO_COLETADOS = [
    {
        "campo": "Nome e sobrenome (first_name, last_name)",
        "situacao": "Existem no modelo padrão do Django, mas o formulário de cadastro não os solicita; ficam vazios",
    },
    {
        "campo": "CPF, data de nascimento, endereço e foto",
        "situacao": "Não existem no modelo de usuário e não são solicitados",
    },
]