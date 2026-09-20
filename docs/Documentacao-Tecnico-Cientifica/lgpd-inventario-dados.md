# LGPD — Inventário de dados pessoais (itens 4.1 a 4.3)

## 1. Dados pessoais tratados (4.1) e suas finalidades (4.2)

| Dado | Origem | Onde fica | Finalidade | Base legal |
|---|---|---|---|---|
| E-mail | Informado no cadastro | `usuarios_usuario.email` | Identificar o titular, autenticar o login (RF02) e enviar o link de recuperação de senha | Execução de contrato (art. 7º, V) |
| Senha | Informada no cadastro | `usuarios_usuario.password` (somente o hash) | Autenticar o titular | Execução de contrato (art. 7º, V) |
| Nome de usuário (`username`) | Preenchido automaticamente com o e-mail | `usuarios_usuario.username` | Exigência técnica do modelo de usuário do Django; não é usado no login | Execução de contrato (art. 7º, V) |
| Telefone (opcional) | Informado pelo titular | `usuarios_usuario.telefone` (criptografado) | Contato com o titular | Consentimento (art. 7º, I) |
| Datas de criação e último acesso | Geradas pelo sistema | `usuarios_usuario.date_joined` e `last_login` | Controle e segurança da conta | Legítimo interesse (art. 7º, IX) |
| Dados do 2FA | Gerados ao ativar a verificação em duas etapas | Tabelas do django-otp | Verificação em duas etapas no login | Legítimo interesse (art. 7º, IX) |
| Sessão e cookies técnicos | Gerados no login | `django_session`; cookies `sessionid` e `csrftoken` | Manter o titular autenticado e proteger os formulários | Execução de contrato (art. 7º, V) |
| Tentativas de login | Geradas pelo django-axes | Tabelas do django-axes (usuário informado, IP, navegador, data) | Proteção contra força bruta | Legítimo interesse (art. 7º, IX) |
| Log de recuperação de senha | Gerado pelo sistema | `logs/recuperacao_senha.log` (e-mail informado e data) | Auditoria do fluxo de recuperação | Legítimo interesse (art. 7º, IX) |
| Registros de acesso da hospedagem | Gerados por Render e Cloudflare | Infraestrutura de terceiros (IP, URL, navegador) | Operação e segurança da hospedagem | Legítimo interesse (art. 7º, IX) |
| Consentimentos e solicitações do titular | Gerados pelo módulo LGPD | `lgpd_registroconsentimento` e `lgpd_solicitacaotitular` | Comprovar o consentimento e o atendimento dos direitos | Obrigação legal (art. 7º, II; art. 8º, §2º) |

As bases legais são a proposta do grupo, com base na Lei nº 13.709/2018 (LGPD), e devem ser validadas pelo professor responsável.

A mesma lista existe em código, em `lgpd/inventario.py`, e alimenta a página "Meus dados" do sistema.

## 2. Evidência de minimização de dados (4.3)

- O formulário de cadastro solicita apenas **e-mail e senha**.
- Nome e sobrenome existem no modelo padrão do Django, mas **não são solicitados** e ficam vazios.
- CPF, data de nascimento, endereço e foto **não existem** no modelo de usuário.
- O telefone é **opcional** e, quando informado, fica criptografado em repouso.
- A senha **nunca** é guardada em texto puro (hash PBKDF2-SHA256 com salt).
- O `username` é uma cópia do e-mail, mantida apenas porque o modelo `AbstractUser` do Django a exige.

Evidências em `docs/Evidencias/lgpd/`:

- `print-cadastro-campos-minimos.jpg`: tela de cadastro com apenas e-mail e senha.
- `print-minimizacao-usuario-shell.jpg`: usuário criado pelo formulário, com nome, sobrenome e telefone vazios.

## 3. Proteção e retenção

| Dado | Proteção | Retenção |
|---|---|---|
| E-mail, senha e nome de usuário | HTTPS; hash com salt para a senha | Enquanto a conta existir |
| Telefone | Criptografia Fernet; chave separada | Até revogar o consentimento ou excluir a conta |
| Dados do 2FA | Acesso restrito ao banco | Até desativar o 2FA ou excluir a conta |
| Sessão | Cookie HttpOnly e Secure | Até a sessão expirar |
| Tentativas de login | Acesso restrito ao banco | A definir pelo grupo |
| Log de recuperação de senha | Arquivo fora do repositório | Enquanto o arquivo existir |
| Registros da hospedagem | Gerenciados pelos provedores | Conforme a política de cada provedor |
| Consentimentos e solicitações | Acesso restrito ao banco | Consentimentos: apagados com a conta. Solicitações: mantidas sem dados pessoais |

---

> Última atualização: _(20/09/2026)_
> Responsável pela documentação: _(Beatriz Miguel)_