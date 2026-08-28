# Requisitos Funcionais e Não Funcionais

**Projeto Nivela — Versão 3 (ajustada)**

Este documento apresenta a versão 3 dos Requisitos Funcionais (RF) e Requisitos Não Funcionais (RNF) do projeto Nivela, revisando a versão 2 a partir do confronto com o Termo de Abertura do Projeto (TAP) v1. Itens novos ou ajustados estão sinalizados com **(NOVO)** ou **(AJUSTADO)**.

> **Resumo quantitativo:** 51 Requisitos Funcionais (46 da v2 + 5 novos), 31 Requisitos Não Funcionais (com 3 ajustes de redação/meta) e 6 Critérios de Aceite.

## 1. Requisitos Funcionais (RF)

### 1.1 Autenticação e Gestão de Perfis

| ID | Descrição |
|----|-----------|
| RF01 | O sistema deve permitir o cadastro de novos usuários (estudante, professor e administrador), com validação dos dados informados. |
| RF02 | O sistema deve permitir o login por e-mail e senha, de forma segura. |
| RF03 | O sistema deve controlar o acesso às funcionalidades com base em perfis de usuário (RBAC): estudante, professor e administrador. |
| RF04 | O sistema deve permitir a recuperação e redefinição de senha. |
| RF05 | O sistema deve permitir que o usuário edite os dados do próprio perfil. |
| RF06 | O sistema deve permitir que o usuário faça upload e atualize sua foto de perfil. |
| **RF07 (AJUSTADO)** | O sistema deve implementar autenticação de dois fatores (2FA) para os usuários. **Prioridade rebaixada para desejável** — candidato a postergação para uma versão futura, caso o cronograma da disciplina não comporte o esforço de implementação. |
| **RF08 (AJUSTADO)** | Caso o 2FA (RF07) seja implementado, o sistema deve validar o segundo fator somente após a validação bem-sucedida da autenticação primária (e-mail e senha). |
| RF09 | O sistema deve invalidar a sessão do usuário ao realizar logout. |
| RF10 | O sistema deve exigir o aceite explícito dos Termos de Uso e da Política de Privacidade no momento do cadastro. |
| RF11 | O sistema deve permitir que o usuário solicite a exclusão da própria conta e dos dados pessoais associados. |
| RF12 | O sistema deve permitir que o usuário exporte seus dados pessoais em formato legível (portabilidade de dados, conforme LGPD). |

### 1.2 Diagnóstico e Nivelamento

| ID | Descrição |
|----|-----------|
| RF13 | O sistema deve aplicar um teste de diagnóstico inicial ao estudante recém-cadastrado. |
| RF14 | O sistema deve classificar automaticamente o nível de conhecimento do estudante a partir do resultado do diagnóstico. |
| RF15 | O sistema deve permitir a reaplicação periódica do diagnóstico, para acompanhar a evolução do estudante ao longo do tempo. |
| RF16 | O sistema deve apresentar ao professor um panorama consolidado do nivelamento de toda a turma. |
| RF17 | O sistema deve permitir que o administrador configure e ajuste os critérios de classificação do diagnóstico. |
| RF18 | O sistema deve permitir a exportação do relatório de diagnóstico do estudante ou da turma em formato PDF. |

### 1.3 Módulo Pedagógico (Trilhas, Atividades e Gamificação)

| ID | Descrição |
|----|-----------|
| RF19 | O sistema deve recomendar trilhas de aprendizagem personalizadas de acordo com o nível identificado do estudante. |
| RF20 | O sistema deve disponibilizar conteúdos de microaprendizagem e exercícios práticos vinculados às trilhas. |
| RF21 | O sistema deve registrar e exibir o progresso do estudante em cada trilha e atividade. |
| RF22 | O sistema deve atribuir pontuações e conquistas de gamificação conforme o desempenho e o engajamento do estudante. |
| RF23 | O sistema deve exibir ao estudante um dashboard pessoal com seu progresso e pontuação. |
| RF24 | O sistema deve permitir que o professor ou administrador configure novas conquistas e regras de pontuação. |
| RF25 | O sistema deve permitir que o estudante envie feedback sobre uma atividade ou trilha concluída. |
| **RF47 (NOVO)** | O sistema deve permitir que o estudante submeta respostas a atividades práticas vinculadas a uma trilha (texto, arquivo ou resposta objetiva, conforme o tipo de atividade). |
| **RF48 (NOVO)** | O sistema deve permitir que o professor visualize, corrija e avalie as atividades práticas submetidas pelos estudantes, registrando nota ou parecer. |

### 1.4 Grupos e Monitoria entre Pares

| ID | Descrição |
|----|-----------|
| RF26 | O sistema deve sugerir a formação de grupos de estudo equilibrados, com base nos níveis de conhecimento diagnosticados. |
| RF27 | O sistema deve permitir que estudantes solicitem ou ofereçam monitoria entre pares. |
| RF28 | O sistema deve permitir que o professor supervisione e medie os grupos formados e as monitorias em andamento. |
| RF29 | O sistema deve permitir que o estudante participe de grupos sugeridos pela plataforma. |
| RF30 | O sistema deve permitir que os estudantes avaliem a monitoria recebida ao final da sessão. |
| **RF49 (NOVO)** | O sistema deve identificar e sugerir, de forma proativa, estudantes aptos a atuar como monitores em um tema, com base no desempenho diagnosticado, permitindo que sejam convidados pelo professor ou pelos colegas. |

### 1.5 Comunicação

| ID | Descrição |
|----|-----------|
| RF31 | O sistema deve disponibilizar um chat integrado para comunicação entre estudantes e professores. |
| RF32 | O sistema deve notificar os usuários, dentro da plataforma, sobre eventos relevantes (nova trilha liberada, convite de grupo, nova mensagem, etc.). |
| RF33 | O sistema deve enviar notificações por e-mail para eventos configurados como críticos (ex.: redefinição de senha, convite de monitoria). |
| RF34 | O sistema deve permitir a consulta ao histórico de mensagens trocadas no chat. |

### 1.6 Gestão do Professor

| ID | Descrição |
|----|-----------|
| RF35 | O sistema deve permitir que o professor crie e gerencie suas turmas. |
| RF36 | O sistema deve permitir que o professor crie e edite atividades e trilhas de aprendizagem. |
| RF37 | O sistema deve exibir ao professor um dashboard analítico com os resultados dos diagnósticos e a evolução da turma. |
| RF38 | O sistema deve identificar automaticamente dificuldades recorrentes apresentadas pela turma. |
| RF39 | O sistema deve permitir a exportação de relatórios de turma em formato PDF ou planilha (Excel/CSV). |
| RF40 | O sistema deve permitir que o professor reutilize e organize um banco próprio de questões e atividades. |

### 1.7 Administração do Sistema

| ID | Descrição |
|----|-----------|
| RF41 | O sistema deve permitir que o administrador gerencie globalmente usuários e perfis de acesso. |
| RF42 | O sistema deve permitir que o administrador realize a manutenção e parametrização geral da plataforma. |
| RF43 | O sistema deve registrar logs de auditoria das ações administrativas realizadas (quem, o quê, quando). |
| RF44 | O sistema deve permitir que o administrador configure a política de retenção e descarte de dados da plataforma. |

### 1.8 Onboarding e Acessibilidade

| ID | Descrição |
|----|-----------|
| RF45 | O sistema deve apresentar um tutorial guiado de onboarding no primeiro acesso do usuário. |
| RF46 | O sistema deve oferecer opções de acessibilidade configuráveis pelo usuário (alto contraste e ajuste de tamanho de fonte). |

### 1.9 Consentimento e Acompanhamento por Responsáveis Legais (NOVO)

| ID | Descrição |
|----|-----------|
| **RF50 (NOVO)** | Para estudantes menores de idade, o sistema deve coletar o consentimento específico de um responsável legal antes de tratar os dados pessoais do menor, conforme art. 14 da LGPD. |
| **RF51 (NOVO — desejável)** | O sistema deve permitir que um responsável legal tenha acesso de leitura ao progresso e à evolução do estudante menor sob sua responsabilidade. Requisito desejável, podendo ser postergado para uma versão futura caso o prazo do MVP não comporte. |

## 2. Requisitos Não Funcionais (RNF)

### 2.1 Usabilidade

| ID | Descrição |
|----|-----------|
| RNF01 | A interface deve ser responsiva, funcionando corretamente em navegadores desktop e dispositivos móveis. |
| RNF02 | A interface deve ser intuitiva e amigável, validada por meio de testes de usabilidade com usuários beta. |
| RNF03 | A interface deve estar em conformidade com as diretrizes de acessibilidade WCAG 2.1, nível AA. |
| RNF04 | O idioma padrão da interface deve ser o Português do Brasil (pt-BR). |

### 2.2 Segurança e Privacidade (LGPD)

| ID | Descrição |
|----|-----------|
| RNF05 | Dados sensíveis devem ser criptografados em trânsito (HTTPS/TLS) e em repouso. |
| RNF06 | O controle de acesso deve seguir o modelo RBAC (Role-Based Access Control). |
| RNF07 | O sistema deve estar em conformidade com a LGPD: consentimento explícito no cadastro, anonimização de dados para fins estatísticos e aplicação dos princípios de finalidade, adequação e necessidade. |
| RNF08 | Por tratar dados de estudantes menores de idade, o sistema deve adotar controles adicionais de proteção de dados (Privacy by Design), incluindo o consentimento do responsável legal previsto no RF50. |
| RNF09 | O sistema deve ter uma política de retenção e descarte de dados definida e documentada, incluindo prazos por tipo de dado. |
| RNF10 | As senhas dos usuários devem ser armazenadas utilizando hash criptográfico seguro (Argon2, bcrypt ou PBKDF2), nunca em texto plano. |
| RNF11 | Os parâmetros de custo do algoritmo de hash (ex.: número de iterações, memória, paralelismo) devem ser configurados adequadamente e justificados tecnicamente. |
| RNF12 | Cada senha deve ser protegida por um salt criptográfico único por usuário. |
| RNF13 | O hash da senha e o respectivo salt devem ser armazenados de forma correta e segura no banco de dados. |
| RNF14 | As sessões de usuário devem possuir tempo de expiração definido. |
| RNF15 | O sistema deve implementar proteção contra ataques de força bruta no login, por meio de rate limiting, bloqueio temporário de conta e/ou atraso progressivo entre tentativas. |
| RNF16 | O sistema deve registrar logs de eventos de autenticação (login, logout e tentativas de acesso malsucedidas). |

### 2.3 Desempenho

| ID | Descrição |
|----|-----------|
| RNF17 | As funcionalidades principais (login, dashboard, chat) devem responder em até 2 segundos para 95% das requisições em condições normais de uso. |
| RNF18 | O sistema deve suportar, no mínimo, 40 usuários simultâneos de uma mesma turma sem degradação perceptível de desempenho. |
| RNF19 | A arquitetura deve permitir escalabilidade horizontal para suportar o crescimento do número de turmas e usuários concorrentes, na medida do viável dentro do free tier utilizado (ver RNF29–RNF31). |

### 2.4 Confiabilidade e Disponibilidade

| ID | Descrição |
|----|-----------|
| **RNF20 (AJUSTADO)** | O sistema deve manter um esforço de disponibilidade compatível com a infraestrutura gratuita utilizada, sem interrupções não planejadas superiores a algumas horas durante o período letivo. A meta anterior de 99% foi removida por ser incompatível com a restrição orçamentária do projeto (RNF29). |
| **RNF21 (AJUSTADO)** | O sistema deve realizar backup do banco de dados ao menos semanalmente, de forma manual ou automatizada, compatível com o orçamento nulo do projeto. |
| **RNF22 (AJUSTADO)** | O procedimento de restauração do backup (RNF21) deve estar documentado, dispensando metas formais de RTO/RPO nível empresarial, incompatíveis com o escopo de MVP acadêmico. |

### 2.5 Compatibilidade

| ID | Descrição |
|----|-----------|
| RNF23 | O sistema deve ser compatível com as duas últimas versões estáveis dos principais navegadores web (Chrome, Firefox, Edge e Safari). |
| RNF24 | O sistema deve suportar corretamente resoluções de tela móveis a partir de 360px de largura. |

### 2.6 Manutenibilidade

| ID | Descrição |
|----|-----------|
| RNF25 | O código-fonte deve ser documentado e seguir boas práticas de engenharia de software. |
| RNF26 | A arquitetura do sistema deve ser modular, permitindo a evolução e inclusão de novos módulos no futuro. |
| RNF27 | O sistema deve possuir cobertura mínima de testes automatizados para os módulos críticos (autenticação, diagnóstico e segurança). |
| RNF28 | O projeto deve utilizar controle de versão (Git) e um pipeline de integração contínua (CI) para build e testes. |

### 2.7 Custo e Infraestrutura

| ID | Descrição |
|----|-----------|
| RNF29 | O desenvolvimento deve utilizar ferramentas, frameworks e serviços gratuitos ou open-source, em razão do orçamento nulo/limitado do projeto. |
| RNF30 | Serviços de nuvem utilizados devem se manter dentro de camadas gratuitas (free tier) ou de baixíssimo custo. |
| RNF31 | O sistema deve monitorar o consumo dos serviços em nuvem e alertar a equipe quando o uso se aproximar dos limites do free tier. |

## 3. Critérios de Aceite e Documentação

| ID | Descrição |
|----|-----------|
| ACE01 | O fluxo de autenticação (incluindo 2FA, se implementado) deve estar documentado. |
| ACE02 | Devem ser apresentadas evidências funcionais da autenticação (prints de tela, logs de sistema ou testes automatizados). |
| ACE03 | As justificativas técnicas das escolhas de segurança (algoritmo de hash, parâmetros de custo, estratégia de 2FA, etc.) devem estar documentadas. |
| ACE04 | O critério/algoritmo de classificação do diagnóstico (RF14, RF17) deve estar documentado e ser auditável. |
| ACE05 | Devem ser apresentadas evidências de testes de desempenho que comprovem o atendimento aos RNF17–RNF19 (ex.: relatório de teste de carga). |
| **ACE06 (AJUSTADO)** | O procedimento de backup e restauração (RNF21–RNF22) deve estar documentado. |

## 4. O que mudou em relação à Versão 2

**Requisitos funcionais adicionados:**
- **RF47 e RF48** — submissão de atividades práticas pelo estudante e correção/avaliação pelo professor, cobrindo a dor "desconexão entre teoria e prática" citada no TAP e antes sem RF correspondente.
- **RF49** — sugestão proativa de monitores pelo sistema, atendendo ao objetivo específico "Potencializar a colaboração" e ao trecho do TAP que prevê alunos "convidados" a monitorar (não só quem se oferece).
- **RF50** — consentimento específico do responsável legal para tratamento de dados de estudantes menores, exigência do art. 14 da LGPD, alinhando o documento ao stakeholder "Responsáveis (Pais)" citado no TAP.
- **RF51 (desejável)** — acesso de leitura do responsável legal ao progresso do estudante menor, dando alguma funcionalidade ao stakeholder "Responsáveis", que antes não tinha nenhuma no RF/RNF.

**Requisitos ajustados:**
- **RF07/RF08** — 2FA rebaixado de obrigatório para desejável, por não constar no TAP e representar risco de esforço frente ao prazo da equipe de 3 integrantes.
- **RNF20** — meta de 99% de disponibilidade suavizada, por ser incompatível com a restrição de orçamento nulo declarada no próprio TAP (RNF29).
- **RNF21/RNF22** — política de backup e disaster recovery simplificada de nível empresarial (RTO/RPO) para algo proporcional a um MVP acadêmico.
- **ACE06** — critério de aceite ajustado para refletir a simplificação de RNF21/RNF22.

**Observação de rastreabilidade:**
Todos os itens novos foram derivados diretamente de trechos do TAP v1 (seção 3 — Definição do Problema; seção 6 — Descrição da Solução; seção 13 — Stakeholders) que ainda não tinham requisito funcional correspondente na v2.
