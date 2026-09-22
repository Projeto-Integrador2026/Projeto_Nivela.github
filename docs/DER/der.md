# Modelagem do Banco de Dados (DER) — Projeto Nivela

> Documento alinhado ao script SQL (PostgreSQL) fornecido pela equipe, derivado dos Requisitos Funcionais e Não Funcionais v3. Reflete o schema completo planejado para o MVP.

## 1. Entidades e atributos (por módulo)

### 1.1 Autenticação e Gestão de Perfis (RF01–RF12, RF50–RF51)

**usuarios** — ✅ Implementado (confirmado via migrações aplicadas no PostgreSQL)
| Atributo | Tipo | Descrição |
|----------|------|-----------|
| id | BIGSERIAL (PK) | Identificador único |
| nome | VARCHAR(150) | Nome completo |
| email | VARCHAR(150), único | Usado para login |
| senha_hash | VARCHAR(255) | Hash da senha (RNF10) |
| senha_salt | VARCHAR(255) | Salt único por usuário (RNF12) |
| tipo_perfil | VARCHAR(20) | estudante \| professor \| administrador (RBAC — RF03) |
| foto_perfil_url | VARCHAR(255) | RF06 |
| data_nascimento | DATE | Usado para identificar menores de idade (RF50) |
| aceite_termos_em | TIMESTAMP | RF10 |
| dois_fatores_ativo | BOOLEAN | RF07 — 2FA obrigatório |
| ativo | BOOLEAN | Falso após exclusão de conta (RF11) |

**tokens_redefinicao_senha** — ✅ Implementado (RF04, recuperação de senha já documentada em `fluxo-recuperacao-senha.md`)

**responsaveis_legais** — ❌ Planejado, ainda não implementado (depende do módulo LGPD)

**consentimentos_responsavel** — ❌ Planejado, ainda não implementado (RF50, depende do módulo LGPD)

> ✅ Tabelas de infraestrutura de segurança já confirmadas via migrações: `django_axes` (proteção contra força bruta), `otp_static`/`otp_totp` (2FA), `django_session` (sessões), `two_factor` (fluxo de autenticação de dois fatores) — geradas automaticamente pelas bibliotecas django-axes, django-otp e django-two-factor-auth.

### 1.2 Turmas e Matrículas (RF35)

**turmas** — ✅ Implementado (app `turmas` já existe no projeto)
**matriculas** — ⏳ A confirmar se já implementado dentro do app `turmas`

### 1.3 Diagnóstico e Nivelamento (RF13–RF18)

**niveis, diagnosticos, diagnostico_perguntas, diagnostico_alternativas, diagnostico_aplicacoes, diagnostico_respostas_itens** — ⏳ A confirmar localização (não existe um app `diagnostico` separado; lógica provavelmente reside dentro do app `usuarios` ou `turmas`)

### 1.4 Módulo Pedagógico — Trilhas, Lições e Atividades (RF19–RF25, RF47–RF48)

**trilhas, modulos, licoes, blocos_conteudo, atividades_praticas, submissoes_atividades, progresso_licoes, feedbacks_atividade** — ❌ Planejado, ainda não confirmado se implementado (não há app dedicado visível; pode estar em `turmas`)

### 1.5 Gamificação (RF22–RF24)

**conquistas, conquistas_obtidas, eventos_pontuacao** — ⏳ App `gamificacao` já existe no projeto; estrutura interna a confirmar

### 1.6 Grupos e Monitoria entre Pares (RF26–RF30, RF49)

**grupos_estudo, grupos_membros, monitorias, avaliacoes_monitoria, indicacoes_monitor** — ❌ Planejado, ainda não implementado

### 1.7 Comunicação (RF31–RF34)

**mensagens_chat, notificacoes** — ⏳ App `chat` já existe no projeto; estrutura interna a confirmar

### 1.8 Auditoria (RF43, RNF16)

**logs_auditoria** — ⏳ A confirmar; parte do registro de auditoria já pode estar coberta pelos logs do django-axes e pelo `recuperacao_senha.log`

## 2. Relacionamentos e cardinalidade

| Relacionamento | Cardinalidade |
|---|---|
| usuarios (professor) 1 → N turmas | Um professor gerencia várias turmas |
| usuarios (estudante) N ↔ N turmas (via matriculas) | Um estudante pode estar em várias turmas |
| responsaveis_legais 1 → N consentimentos_responsavel | Um responsável pode ter mais de um estudante sob sua responsabilidade |
| usuarios (estudante) 1 → N diagnostico_aplicacoes | Reaplicação periódica do diagnóstico (RF15) |
| diagnosticos 1 → N diagnostico_perguntas → N diagnostico_alternativas | Estrutura do teste de diagnóstico |
| trilhas 1 → N modulos 1 → N licoes 1 → N blocos_conteudo | Hierarquia de conteúdo pedagógico |
| licoes 1 → N atividades_praticas 1 → N submissoes_atividades | Uma atividade recebe várias submissões (uma por estudante) |
| usuarios (estudante) N ↔ N licoes (via progresso_licoes) | Progresso individual por lição |
| usuarios (estudante) N ↔ N conquistas (via conquistas_obtidas) | Um estudante pode ter várias conquistas |
| usuarios (estudante) 1 → N eventos_pontuacao | Histórico de pontuação do estudante |
| turmas 1 → N grupos_estudo | Uma turma pode ter vários grupos |
| grupos_estudo N ↔ N usuarios (estudante, via grupos_membros) | Um grupo tem vários estudantes |
| usuarios 1 → N monitorias (como solicitante ou monitor) | Um usuário participa de várias monitorias |
| monitorias 1 → 1 avaliacoes_monitoria | Cada monitoria tem no máximo uma avaliação |
| usuarios 1 → N mensagens_chat (como remetente) | Um usuário envia várias mensagens |
| usuarios 1 → N notificacoes | Um usuário recebe várias notificações |
| usuarios 1 → N logs_auditoria | Ações de um usuário são registradas em log |

## 3. Diagrama Entidade-Relacionamento
_Insira aqui a imagem do DER, gerada a partir do script SQL (ex: via dbdiagram.io, importando o schema, ou pgAdmin com engenharia reversa)._


## 4. Dicionário de dados (campos sensíveis)

| Tabela | Campo | Tipo | Nulo? | Descrição |
|--------|-------|------|-------|-----------|
| usuarios | senha_hash | VARCHAR(255) | Não | Nunca armazenar senha em texto plano (RNF10) |
| usuarios | senha_salt | VARCHAR(255) | Não | Único por usuário (RNF12) |
| usuarios | tipo_perfil | VARCHAR(20) | Não | estudante \| professor \| administrador (RBAC — RNF06) |
| usuarios | data_nascimento | DATE | Sim | Usado para acionar o fluxo de consentimento (RF50) |
| consentimentos_responsavel | ip_registro | VARCHAR(45) | Sim | Evidência do consentimento (RNF07/RF50) |
| logs_auditoria | acao | VARCHAR(50) | Não | login \| login_falhou \| logout \| alterou_permissao (RNF16) |

## 5. Status de implementação (resumo)

| Categoria | Status |
|-----------|--------|
| Autenticação (usuarios, sessões, 2FA, força bruta) | ✅ Implementado |
| Recuperação de senha (tokens) | ✅ Implementado |
| Turmas | ✅ App existe, estrutura interna a confirmar |
| Diagnóstico e Nivelamento | ⏳ A localizar dentro dos apps existentes |
| Módulo Pedagógico (trilhas, atividades) | ❌ Planejado |
| Gamificação | ✅ App existe, estrutura interna a confirmar |
| Grupos e Monitoria | ❌ Planejado |
| Comunicação (chat) | ✅ App existe, estrutura interna a confirmar |
| LGPD (responsáveis legais, consentimento) | ❌ Planejado |
| Auditoria | ⏳ Parcial (logs de segurança já existem) |

## 6. Observações de rastreabilidade

- Este documento representa o **schema completo planejado** para o MVP, conforme SQL fornecido pela equipe.
- A tabela `SolicitacaoDados` (exportação/exclusão de dados, RF11/RF12) ainda não consta no script SQL e precisa ser adicionada quando o módulo LGPD for desenvolvido.
- Recomenda-se, conforme cada módulo for implementado, atualizar a coluna de status deste documento e gerar o diagrama visual real a partir do schema aplicado no banco (via pgAdmin, clicando com o botão direito no banco `nivela_db` → "Generate ER Diagram", se disponível na versão do pgAdmin).

---

> Última atualização: _(22/09/2026)_
> Responsável pela documentação: _(Jhonathan Tonello)_
