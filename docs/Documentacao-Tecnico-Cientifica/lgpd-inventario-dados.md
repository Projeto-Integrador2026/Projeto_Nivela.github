# LGPD — Inventário de dados pessoais (itens 4.1 a 4.11)

## 1. Dados pessoais tratados (4.1) e suas finalidades (4.2)

| Dado | Origem | Onde fica | Finalidade | Base legal |
|---|---|---|---|---|
| E-mail | Informado no cadastro | `usuarios_usuario.email` | Identificar o titular, autenticar o login (RF02) e enviar o link de recuperação de senha | Execução de contrato (art. 7º, V) |
| Senha | Informada no cadastro | `usuarios_usuario.password` (somente o hash) | Autenticar o titular | Execução de contrato (art. 7º, V) |
| Nome de usuário (`username`) | Preenchido automaticamente com o e-mail | `usuarios_usuario.username` | Exigência técnica do modelo de usuário do Django; não é usado no login | Execução de contrato (art. 7º, V) |
| Telefone (opcional) | Informado pelo titular; hoje só pode ser preenchido via admin, sem tela própria | `usuarios_usuario.telefone` (criptografado) | Contato com o titular | Consentimento (art. 7º, I) |
| Datas de criação e último acesso | Geradas pelo sistema | `usuarios_usuario.date_joined` e `last_login` | Controle e segurança da conta | Legítimo interesse (art. 7º, IX) |
| Dados do 2FA | Gerados ao ativar a verificação em duas etapas | Tabelas do django-otp | Verificação em duas etapas no login | Legítimo interesse (art. 7º, IX) |
| Sessão e cookies técnicos | Gerados no login | `django_session`; cookies `sessionid` e `csrftoken` | Manter o titular autenticado e proteger os formulários | Execução de contrato (art. 7º, V) |
| Tentativas de login | Geradas pelo django-axes | Tabelas do django-axes (usuário informado, IP, navegador, data) | Proteção contra força bruta | Legítimo interesse (art. 7º, IX) |
| Log de recuperação de senha | Gerado pelo sistema | `logs/recuperacao_senha.log` (e-mail informado e data) | Auditoria do fluxo de recuperação | Legítimo interesse (art. 7º, IX) |
| Registros de acesso da hospedagem | Gerados por Render e Cloudflare | Infraestrutura de terceiros (IP, URL, navegador) | Operação e segurança da hospedagem | Legítimo interesse (art. 7º, IX) |
| Progresso nas lições | Gerado pelo sistema conforme o titular avança | `gamificacao_progressolicao` (usuário, lição, concluída, data) | Controlar o avanço na trilha de aprendizado | Execução de contrato (art. 7º, V) |
| Tentativas de exercícios | Geradas a cada resposta do titular | `gamificacao_tentativaexercicio` (usuário, exercício, correta, data) | Avaliar desempenho e liberar próximos módulos | Execução de contrato (art. 7º, V) |
| Perfil de gamificação (XP, streak, última atividade) | Calculado pelo sistema a partir do uso | `gamificacao_perfilgamificacao` | Ranking, nível e sequência de estudo | Execução de contrato (art. 7º, V) |
| Resultado do teste de nivelamento e liberações manuais | Gerado pelo sistema (teste) ou por um professor | `gamificacao_resultadonivelamento` e `gamificacao_liberacaomanual` | Definir módulo inicial e registrar liberações do professor | Legítimo interesse (art. 7º, IX) |
| Consentimentos e solicitações do titular | Gerados pelo módulo LGPD | `lgpd_registroconsentimento` e `lgpd_solicitacaotitular` | Comprovar o consentimento e o atendimento dos direitos | Obrigação legal (art. 7º, II; art. 8º, §2º) |

As bases legais são a proposta do grupo, com base na Lei nº 13.709/2018 (LGPD), e devem ser validadas pelo professor responsável.

A mesma lista existe em código, em `lgpd/inventario.py`, e alimenta a página "Meus dados" do sistema.

Cada linha da tabela acima traz uma finalidade específica (coluna "Finalidade"), atendendo ao item 4.2: nenhum dado é tratado sem um propósito claro e definido, e nenhuma finalidade é genérica ou compartilhada indevidamente entre dados de natureza diferente.

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
| Progresso, tentativas, perfil de gamificação e nivelamento | Acesso restrito ao banco | Enquanto a conta existir |
| Consentimentos e solicitações | Acesso restrito ao banco | Consentimentos: apagados com a conta. Solicitações: mantidas sem dados pessoais |

---

> Última atualização: _(20/09/2026)_
> Responsável pela documentação: _(Beatriz Miguel)_


## 4. Registro explícito de consentimento (4.4)

- No cadastro (`/cadastro/`), o titular precisa marcar obrigatoriamente a caixa "Li e aceito os Termos de Uso e a Política de Privacidade" (`aceite_termos` em `usuarios/forms.py`). O campo vem **desmarcado por padrão** e o cadastro não é concluído sem essa ação afirmativa.
- Ao concluir o cadastro, `usuarios/views.py` (`CadastroView.form_valid`) cria automaticamente um registro em `RegistroConsentimento` (`lgpd/models.py`), com:
  - `finalidade = "termos_uso"`
  - `versao_termo` = versão vigente dos termos no momento (`VERSAO_TERMOS` em `lgpd/inventario.py`)
  - `concedido = True` e `data_concessao` = data/hora do cadastro
- Esse registro fica visível no Django Admin, em **LGPD → Registros de consentimento**.

Evidências em `docs/Evidencias/lgpd/`:

- `print-consentimento-checkbox-obrigatorio.jpg`: tentativa de cadastro sem marcar o checkbox, recusada com "Este campo é obrigatório."
- `print-consentimento-registrado-admin.jpg`: registro de consentimento criado no Admin após o cadastro com o checkbox marcado.


## 5. Consentimento associado à finalidade (4.5)

O modelo `RegistroConsentimento` (`lgpd/models.py`) obriga cada registro a declarar
uma finalidade específica através do campo `finalidade`, que usa `choices` fixos:

- `termos_uso` — Termos de uso e política de privacidade
- `telefone` — Uso do telefone para contato

Não existe consentimento genérico: todo registro criado no sistema precisa
pertencer a uma dessas finalidades. O registro do item 4.4 é um exemplo prático
disso — a finalidade "Termos de uso e política de privacidade" fica associada
a esse consentimento específico, visível na mesma evidência
`print-consentimento-registrado-admin.jpg`.


## 6. Possibilidade de revogação do consentimento (4.6)

- O titular logado acessa **Meus dados** (menu superior) e vê todos os seus
  consentimentos na tela "Meus consentimentos" (`lgpd/views.py`,
  `meus_consentimentos`), com finalidade, versão do termo, status,
  data de concessão e de revogação.
- Cada consentimento ativo tem um botão **Revogar**, que chama a view
  `revogar_consentimento` (protegida por login e restrita ao próprio titular)
  e usa o método `revogar()` do model `RegistroConsentimento`.
- A revogação **não apaga** o registro: mantém o histórico completo
  (data de concessão original + data da revogação), só marca
  `concedido = False`. Isso atende à rastreabilidade exigida pela LGPD.
- Revogar o consentimento aos Termos de Uso não exclui a conta nem os dados
  do titular — isso é tratado separadamente pela funcionalidade de exclusão
  (item 4.10).

Evidências em `docs/Evidencias/lgpd/`:

- `print-consentimentos-lista-antes-revogar.jpg`: tela "Meus consentimentos" com o consentimento ativo e o botão "Revogar" disponível.
- `print-consentimentos-revogado.jpg`: mesma tela após a revogação, com status "Revogado" e data/hora registrada.


## 7. Registro de data e versão do consentimento (4.7)

- Todo `RegistroConsentimento` grava, no momento em que é criado:
  - `versao_termo`: a versão dos Termos de Uso / Política de Privacidade vigente
    naquele momento, definida em `VERSAO_TERMOS` (`lgpd/inventario.py`). Se o
    texto dos termos mudar no futuro, essa constante deve ser incrementada
    (ex.: "1.1"), preservando nos registros antigos qual versão cada titular
    realmente aceitou.
  - `data_concessao`: data e hora exatas do consentimento, geradas pelo
    sistema (`timezone.now()`), não informadas pelo titular.
- A revogação (item 4.6) segue o mesmo princípio: `data_revogacao` é gravada
  automaticamente pelo método `revogar()` no momento em que o titular clica
  em "Revogar", nunca informada manualmente.
- Essas informações ficam visíveis tanto no Django Admin (**LGPD → Registros
  de consentimento**) quanto para o próprio titular, na tela **Meus dados**
  (item 4.6), que exibe as colunas "Versão do termo", "Concedido em" e
  "Revogado em" para cada registro.

Não há evidência nova para este item: as mesmas evidências dos itens 4.4 e 4.6
(`print-consentimento-registrado-admin.jpg`,
`print-consentimentos-lista-antes-revogar.jpg` e
`print-consentimentos-revogado.jpg`) já mostram a versão e as datas gravadas.


## 8. Funcionalidade de consulta aos dados do titular (4.8)

- O titular logado acessa **Meus dados** (menu superior), que agora leva à tela
  de consulta (`lgpd/views.py`, `meus_dados`), mostrando:
  - **Dados da conta**: e-mail, telefone, data de criação da conta, data do
    último acesso, e se a verificação em duas etapas está ativada.
  - **Dados de aprendizagem e gamificação**: XP total, nível, streak atual,
    streak recorde, quantidade de lições concluídas, quantidade de tentativas
    de exercícios (com acertos) e o resultado do teste de nivelamento.
- A partir dessa tela, o titular também acessa **Meus consentimentos**
  (item 4.6), onde consulta e revoga os consentimentos dados.
- Juntas, essas duas telas cobrem a consulta completa aos dados listados no
  inventário do item 4.1.

Evidência em `docs/Evidencias/lgpd/`:

- `print-meus-dados-consulta.jpg`: tela "Meus dados" exibindo os dados da conta e de gamificação do titular logado.


## 9. Funcionalidade de exportação dos dados (4.9)

- Na tela **Meus dados**, o titular logado tem o botão **"Baixar meus dados
  (JSON)"**, que aciona a view `exportar_dados` (`lgpd/views.py`).
- O arquivo `meus-dados-nivela.json` gerado contém:
  - **Conta**: e-mail, telefone, data de criação e último acesso.
  - **Gamificação**: XP total, nível, streaks, lista completa de lições
    concluídas, tentativas de exercícios e resultados do teste de
    nivelamento (não só os totais mostrados na tela, o histórico inteiro).
  - **Consentimentos**: todos os registros do titular, com finalidade,
    versão do termo e as datas de concessão/revogação.
- O formato JSON é estruturado e de uso comum, atendendo ao requisito de
  portabilidade dos dados (LGPD, art. 18, V).

Evidência em `docs/Evidencias/lgpd/`:

- `print-exportacao-json.jpg`: botão de exportação na tela "Meus dados" e o conteúdo do arquivo `meus-dados-nivela.json` baixado, incluindo o histórico de consentimento do titular.


## 10. Funcionalidade de exclusão dos dados pessoais (4.10)

- Na tela **Meus dados**, o titular logado tem o link **"Excluir minha conta
  e todos os meus dados"**, que leva à tela de confirmação
  (`lgpd/views.py`, `excluir_conta`).
- Antes de excluir, o sistema exige que o titular **confirme a senha atual**
  e **marque uma caixa de confirmação explícita**. Uma senha incorreta
  recusa o pedido sem apagar nada.
- Ao confirmar corretamente, o sistema:
  1. Cria um registro em `SolicitacaoTitular` com um identificador anônimo
     (`uuid4`), tipo "Exclusão dos dados" e status "Concluída".
  2. Apaga a conta (`usuario.delete()`), o que **remove em cascata** (via
     `on_delete=CASCADE` dos models): telefone e demais dados da conta,
     progresso nas lições, tentativas de exercícios, perfil de gamificação
     (XP/streak), resultados de nivelamento e registros de consentimento.
  3. Encerra a sessão do titular (`logout`) e o redireciona para o login,
     com uma mensagem de confirmação exibindo o **protocolo de atendimento**
     (o identificador anônimo).
- O registro em `SolicitacaoTitular` **permanece** depois da exclusão, mas
  com o campo `usuario` nulo (`on_delete=SET_NULL`), preservando a prova de
  que o direito foi atendido sem manter nenhum dado pessoal associado a ela.

Evidências em `docs/Evidencias/lgpd/`:

- `print-exclusao-confirmacao.jpg`: tela de confirmação com o aviso, campo de senha e checkbox.
- `print-exclusao-senha-incorreta.jpg`: tentativa de exclusão com senha errada, recusada.
- `print-exclusao-sucesso.jpg`: mensagem de sucesso na tela de login, com o protocolo de atendimento.
- `print-exclusao-solicitacao-anonima.jpg`: registro em `SolicitacaoTitular` no Admin, com identificador anônimo preservado e usuário nulo.


## 11. Fluxo de atendimento aos direitos do titular (4.11)

O Nivela atende aos direitos do titular (art. 18 da LGPD) por **autoatendimento**:
o próprio titular exerce cada direito diretamente na plataforma, sem precisar
abrir um chamado ou esperar uma pessoa da equipe processar o pedido. Isso faz
com que o atendimento seja **imediato**, bem abaixo do prazo máximo de 15 dias
previsto no art. 19 da LGPD.

| Direito (art. 18, LGPD) | Onde o titular exerce | O que o sistema faz | Prazo |
|---|---|---|---|
| Confirmação do tratamento e acesso aos dados (incisos I e II) | Tela **Meus dados** (4.8) | Exibe em tempo real todos os dados da conta e de gamificação | Imediato |
| Portabilidade dos dados (inciso V) | Botão "Baixar meus dados (JSON)" (4.9) | Gera e entrega o arquivo para download na hora | Imediato |
| Revogação do consentimento (art. 8º, §5º) | Tela **Meus consentimentos** (4.6) | Marca o consentimento como revogado e grava a data | Imediato |
| Eliminação dos dados (inciso VI) | Link "Excluir minha conta e todos os meus dados" (4.10) | Exclui a conta em cascata e registra um protocolo anônimo de atendimento | Imediato |

**Autenticação como salvaguarda:** todos os quatro fluxos exigem que o titular
esteja logado (`@login_required`), e a exclusão exige ainda a senha atual como
segunda confirmação — isso evita que alguém exerça esses direitos em nome de
outra pessoa.

**Prova do atendimento:** o model `SolicitacaoTitular` (`lgpd/models.py`) guarda
o registro formal do pedido mais sensível e irreversível (exclusão), com um
identificador anônimo que sobrevive mesmo depois que os dados pessoais da
pessoa deixam de existir (`on_delete=SET_NULL`). Os demais direitos (acesso,
exportação e revogação) são reversíveis ou não destroem informação, e por
isso sua evidência de atendimento já fica naturalmente nos próprios dados
alterados (ex.: `data_revogacao` em `RegistroConsentimento`) ou nas telas
que os exibem em tempo real.

**Canal alternativo:** hoje não existe um canal humano separado (e-mail de
DPO, formulário de contato) para quem preferir não usar o autoatendimento;
todo o atendimento aos direitos do titular acontece pela própria plataforma.
Isso é registrado aqui como uma limitação conhecida, não coberta pelo
Requisito 4 atual.

Não há evidência nova neste item: as evidências dos itens 4.6, 4.8, 4.9 e
4.10 já demonstram, juntas, o fluxo completo de ponta a ponta.

> Última atualização: _(23/09/2026)_
> Por _(Beatriz Mguel)_