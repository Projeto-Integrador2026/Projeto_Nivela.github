# Diagrama de Casos de Uso — Projeto Nivela

> Documento alinhado ao Termo de Abertura do Projeto (TAP) v1 e aos Requisitos Funcionais e Não Funcionais v3.

## 1. Atores

| Ator | Descrição |
|------|-----------|
| **Estudante** | Usuário que realiza diagnóstico, acessa trilhas de aprendizagem, participa de grupos/monitorias e se comunica via chat |
| **Professor** | Usuário que gerencia turmas, cria atividades/trilhas, acompanha o desempenho da turma e supervisiona monitorias |
| **Administrador** | Usuário responsável pela gestão global de usuários, permissões e parametrização da plataforma |
| **Responsável Legal (NOVO)** | Responsável por um estudante menor de idade; consente com o tratamento de dados e pode acompanhar o progresso do menor |

> Controle de acesso baseado em perfis (RBAC), conforme RF03 e RNF06.

## 2. Casos de uso por módulo

### 2.1 Autenticação e Gestão de Perfis
| Código | Nome do caso de uso | Ator(es) | Requisito relacionado |
|--------|----------------------|----------|--------------------------|
| UC01 | Cadastrar-se na plataforma | Estudante, Professor, Administrador | RF01 |
| UC02 | Realizar login | Estudante, Professor, Administrador | RF02 |
| UC03 | Autenticar com 2FA *(desejável)* | Estudante, Professor, Administrador | RF07, RF08 |
| UC04 | Recuperar senha | Estudante, Professor, Administrador | RF04 |
| UC05 | Editar dados do perfil | Estudante, Professor, Administrador | RF05 |
| UC06 | Atualizar foto de perfil | Estudante, Professor, Administrador | RF06 |
| UC07 | Encerrar sessão (logout) | Estudante, Professor, Administrador | RF09 |
| UC08 | Aceitar Termos de Uso e Política de Privacidade | Estudante, Professor, Administrador | RF10 |
| UC09 | Solicitar exclusão da conta e dos dados (LGPD) | Estudante, Professor, Administrador | RF11 |
| UC10 | Exportar dados pessoais (LGPD) | Estudante, Professor, Administrador | RF12 |

### 2.2 Diagnóstico e Nivelamento
| Código | Nome do caso de uso | Ator(es) | Requisito relacionado |
|--------|----------------------|----------|--------------------------|
| UC11 | Realizar teste de diagnóstico inicial | Estudante | RF13 |
| UC12 | Visualizar classificação de nível | Estudante | RF14 |
| UC13 | Refazer diagnóstico periodicamente | Estudante | RF15 |
| UC14 | Consultar panorama de nivelamento da turma | Professor | RF16 |
| UC15 | Configurar critérios de classificação do diagnóstico | Administrador | RF17 |
| UC16 | Exportar relatório de diagnóstico (PDF) | Estudante, Professor | RF18 |

### 2.3 Módulo Pedagógico (Trilhas, Atividades e Gamificação)
| Código | Nome do caso de uso | Ator(es) | Requisito relacionado |
|--------|----------------------|----------|--------------------------|
| UC17 | Receber trilha de aprendizagem personalizada | Estudante | RF19 |
| UC18 | Acessar conteúdos e exercícios da trilha | Estudante | RF20 |
| UC19 | Acompanhar progresso na trilha/atividade | Estudante | RF21 |
| UC20 | Receber pontuação e conquistas (gamificação) | Estudante | RF22 |
| UC21 | Visualizar dashboard pessoal de progresso | Estudante | RF23 |
| UC22 | Configurar conquistas e regras de pontuação | Professor, Administrador | RF24 |
| UC23 | Enviar feedback sobre atividade/trilha | Estudante | RF25 |
| UC45 **(NOVO)** | Submeter resposta a atividade prática | Estudante | RF47 |
| UC46 **(NOVO)** | Corrigir e avaliar atividade prática submetida | Professor | RF48 |

### 2.4 Grupos e Monitoria entre Pares
| Código | Nome do caso de uso | Ator(es) | Requisito relacionado |
|--------|----------------------|----------|--------------------------|
| UC24 | Receber sugestão de formação de grupo | Estudante | RF26 |
| UC25 | Solicitar ou oferecer monitoria | Estudante | RF27 |
| UC26 | Supervisionar grupos e monitorias | Professor | RF28 |
| UC27 | Participar de grupo sugerido | Estudante | RF29 |
| UC28 | Avaliar monitoria recebida | Estudante | RF30 |
| UC47 **(NOVO)** | Receber sugestão proativa de estudante-monitor | Professor, Estudante | RF49 |
| UC48 **(NOVO)** | Convidar estudante sugerido para monitoria | Professor, Estudante | RF49 |

### 2.5 Comunicação
| Código | Nome do caso de uso | Ator(es) | Requisito relacionado |
|--------|----------------------|----------|--------------------------|
| UC29 | Enviar/receber mensagens via chat | Estudante, Professor | RF31 |
| UC30 | Receber notificação de evento na plataforma | Estudante, Professor | RF32 |
| UC31 | Receber notificação por e-mail (evento crítico) | Estudante, Professor | RF33 |
| UC32 | Consultar histórico de mensagens | Estudante, Professor | RF34 |

### 2.6 Gestão do Professor
| Código | Nome do caso de uso | Ator(es) | Requisito relacionado |
|--------|----------------------|----------|--------------------------|
| UC33 | Criar e gerenciar turma | Professor | RF35 |
| UC34 | Criar/editar atividades e trilhas | Professor | RF36 |
| UC35 | Visualizar dashboard analítico da turma | Professor | RF37 |
| UC36 | Identificar dificuldades recorrentes da turma | Professor | RF38 |
| UC37 | Exportar relatório de turma (PDF/Excel) | Professor | RF39 |
| UC38 | Gerenciar banco próprio de questões/atividades | Professor | RF40 |

### 2.7 Administração do Sistema
| Código | Nome do caso de uso | Ator(es) | Requisito relacionado |
|--------|----------------------|----------|--------------------------|
| UC39 | Gerenciar usuários e perfis de acesso | Administrador | RF41 |
| UC40 | Realizar manutenção/parametrização da plataforma | Administrador | RF42 |
| UC41 | Consultar logs de auditoria administrativa | Administrador | RF43 |
| UC42 | Configurar política de retenção/descarte de dados | Administrador | RF44 |

### 2.8 Onboarding e Acessibilidade
| Código | Nome do caso de uso | Ator(es) | Requisito relacionado |
|--------|----------------------|----------|--------------------------|
| UC43 | Passar pelo tutorial guiado (onboarding) | Estudante, Professor, Administrador | RF45 |
| UC44 | Configurar opções de acessibilidade | Estudante, Professor, Administrador | RF46 |

### 2.9 Consentimento e Acompanhamento por Responsáveis Legais (NOVO)
| Código | Nome do caso de uso | Ator(es) | Requisito relacionado |
|--------|----------------------|----------|--------------------------|
| UC49 **(NOVO)** | Fornecer consentimento para tratamento de dados do menor | Responsável Legal | RF50 |
| UC50 **(NOVO — desejável)** | Consultar progresso do estudante menor | Responsável Legal | RF51 |

## 3. Diagrama


![Diagrama de Casos de Uso](../assets/diagrama-casos-de-uso.png)

## 4. Descrição detalhada dos casos de uso críticos

### UC01 - Cadastrar-se na plataforma
- **Atores:** Estudante, Professor, Administrador
- **Pré-condições:** Usuário não possui conta no sistema
- **Fluxo principal:**
  1. Usuário acessa a tela de cadastro
  2. Usuário preenche os dados solicitados e seleciona seu perfil (estudante/professor)
  3. Usuário aceita os Termos de Uso e a Política de Privacidade (UC08)
  4. Sistema valida os dados e armazena a senha com hash + salt (RNF10–RNF13)
  5. **Se o estudante for menor de idade**, o sistema aciona o fluxo de consentimento do responsável legal (UC49) antes de concluir o cadastro
  6. Sistema confirma o cadastro
- **Fluxo alternativo:**
  1. Dados inválidos → sistema exibe mensagem de erro

### UC02 - Realizar login
- **Atores:** Estudante, Professor, Administrador
- **Fluxo principal:**
  1. Usuário informa e-mail e senha
  2. Sistema valida as credenciais
  3. **Se o 2FA estiver habilitado** (RF07, desejável), sistema solicita o segundo fator (UC03)
  4. Sistema cria a sessão com controle de acesso por perfil (RBAC)
- **Fluxo alternativo:**
  1. Credenciais inválidas → sistema aplica proteção contra força bruta (RNF15)

### UC45 - Submeter resposta a atividade prática
- **Ator:** Estudante
- **Pré-condições:** Estudante possui uma atividade prática disponível na trilha
- **Fluxo principal:**
  1. Estudante acessa a atividade prática vinculada à lição
  2. Estudante envia a resposta (texto, arquivo ou resposta objetiva)
  3. Sistema registra a submissão e notifica o professor (UC30)

### UC46 - Corrigir e avaliar atividade prática submetida
- **Ator:** Professor
- **Pré-condições:** Existe ao menos uma submissão pendente de correção
- **Fluxo principal:**
  1. Professor acessa a lista de submissões da atividade
  2. Professor avalia a resposta e atribui nota e/ou parecer
  3. Sistema registra a correção e notifica o estudante (UC30)

### UC47 - Receber sugestão proativa de estudante-monitor
- **Atores:** Professor, Estudante
- **Pré-condições:** Existem estudantes com diagnóstico avançado em algum tema
- **Fluxo principal:**
  1. Sistema identifica estudantes aptos com base no desempenho diagnosticado (RF14)
  2. Sistema sugere esses estudantes como potenciais monitores para o professor e/ou colegas
  3. Professor ou colega pode convidar o estudante sugerido (UC48)

### UC49 - Fornecer consentimento para tratamento de dados do menor
- **Ator:** Responsável Legal
- **Pré-condições:** Estudante identificado como menor de idade no cadastro
- **Fluxo principal:**
  1. Sistema solicita os dados de contato do responsável legal
  2. Sistema envia solicitação de consentimento ao responsável (RF50, art. 14 da LGPD)
  3. Responsável legal analisa e confirma (ou recusa) o consentimento
  4. Sistema registra a decisão com data e IP, e libera (ou bloqueia) o cadastro do menor
- **Fluxo alternativo:**
  1. Consentimento recusado → cadastro do estudante não é concluído

### UC50 - Consultar progresso do estudante menor *(desejável)*
- **Ator:** Responsável Legal
- **Pré-condições:** Consentimento já concedido (UC49); vínculo entre responsável e estudante estabelecido
- **Fluxo principal:**
  1. Responsável legal acessa a área de acompanhamento
  2. Sistema exibe, em modo somente leitura, o progresso e a evolução do estudante (RF51)

---

> Última atualização: _(27/08/2026)_
> Responsável pela documentação: _(Jhonathan Tonello)_
