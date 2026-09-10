# Visão Geral do Sistema — Projeto Nivela

## 1. Introdução

O Documento de visão geral do sistema **Nivela**, foi desenvolvido como parte do Projeto Integrador 2026, do curso de Engenharia de Software, sob orientação do professor Fabiano M. O projeto é desenvolvido pela equipe composta pelos alunos Beatriz Miguel, Jhonathan Tonello e Vinicius R.

## 2. Descrição do sistema

O Nivela é uma **plataforma web educacional** que centraliza o diagnóstico e o nivelamento contínuo de estudantes, organizando trilhas de aprendizagem, formação de grupos de estudo e monitoria entre pares, com base no nível de conhecimento identificado de cada aluno. O sistema busca resolver a fragmentação de ferramentas educacionais  e a dificuldade dos professores em identificar e atender às diferenças de conhecimento dentro de uma mesma turma.

## 3. Objetivo do sistema

**Objetivo geral:** Desenvolver uma plataforma web educacional focada no diagnóstico e nivelamento contínuo dos estudantes, que centralize trilhas de aprendizagem, promova a formação inteligente de grupos de estudo e viabilize a monitoria colaborativa entre alunos, garantindo ao professor uma visão unificada e analítica da evolução da turma.

**Objetivos específicos:**

- Estruturar o ensino com trilhas de microaprendizagem e atividades práticas
- Engajar os usuários através de gamificação
- Potencializar a colaboração via formação inteligente de grupos de estudo
- Viabilizar monitorias entre estudantes, supervisionadas pelo professor
- Unificar comunicação, gestão de conteúdo e dashboards em um único ecossistema

## 4. Público-alvo

- **Usuários diretos:** Estudantes do Ensino Superior/Tecnico voltado a tecnologia e Professores
- **Clientes potenciais:** Instituições de ensino público ou privado
- **Foco do MVP:** turmas que apresentam grande disparidade de níveis de conhecimento inicial (ensino técnico ou superior)

## 5. Principais funcionalidades

**Para Estudantes:**
- Cadastro e autenticação segura (com 2FA obrigatório)
- Testes de diagnóstico e nivelamento inicial
- Acesso a trilhas de microaprendizagem e exercícios práticos
- Dashboard pessoal de progresso e gamificação
- Chat integrado com professores e colegas
- Solicitação e prestação de monitoria
- Participação em grupos de estudo sugeridos

**Para Professores:**
- Gestão de turmas e criação de atividades/trilhas
- Dashboard analítico com resultados de diagnósticos e evolução da turma
- Identificação de dificuldades recorrentes
- Supervisão de monitorias e grupos formados

**Para Administradores:**
- Gerenciamento global de usuários, perfis e permissões (RBAC)
- Manutenção e parametrização geral da plataforma

## 6. Tecnologias utilizadas

- **Linguagem:** Python
- **Framework:** Django
- **Banco de dados:** PostgreSQL
- **Front-end:** HTML5, CSS3, JavaScript (templates Django)
- **Bibliotecas de segurança:** django-otp e django-two-factor-auth (2FA), django-axes (proteção contra força bruta), python-decouple (variáveis de ambiente)
- **Controle de versão:** Git e GitHub

## 7. Arquitetura do sistema

O sistema segue o padrão **MVT (Model-View-Template)**, padrão do framework Django, organizado de forma modular, separando em apps independentes:
- **usuarios** — cadastro, autenticação, 2FA e gestão de perfis (RBAC)
- **turmas** — gestão de turmas e matrículas
- **chat** — comunicação entre estudantes e professores
- **gamificacao** — pontuação, conquistas e progresso do estudante


## 8. Ativos do sistema

| Ativo | Descrição | Nível de criticidade |
|-------|-----------|------------------------|
| Dados de autenticação (senha, salt) | Hash PBKDF2 + salt armazenados no banco | Crítico |
| Dados pessoais de usuários | Nome, e-mail, data de nascimento | Alto |
| Dados de menores de idade | Estudantes menores, sujeitos a consentimento do responsável (LGPD) | Crítico |
| Sessões de usuário | Tokens de sessão ativos | Alto |
| Banco de dados (PostgreSQL) | Armazena todos os dados da aplicação | Crítico |
| Configuração 2FA | Segredos/tokens do segundo fator de autenticação | Crítico |
| Logs de auditoria | Registros de autenticação e ações administrativas | Médio |

## 9. Ameaças e vulnerabilidades identificadas

| Ameaça | Descrição | Contramedida |
|--------|-----------|----------------|
| Ataque de força bruta no login | Tentativas repetidas de adivinhar senha | django-axes: bloqueio após 5 tentativas, cooloff de 1h |
| Vazamento de senha em texto plano | Senha armazenada sem proteção | Hash PBKDF2 com salt único por usuário |
| Sequestro de sessão | Reutilização de sessão após logout | Invalidação de sessão no servidor ao encerrar (RF09) |
| Acesso não autorizado a dados de menores | Tratamento de dados sem consentimento | Consentimento obrigatório do responsável legal (RF50) |
| Bypass de autenticação | Acesso sem completar a autenticação completa | 2FA obrigatório via middleware, aplicado a todos os perfis |

## 10. Referências

PINHEIRO, Patricia Peck. Proteção de Dados Pessoais: Comentários à Lei n. 13.709/2018 (LGPD). 5. ed. São Paulo: Saraiva Jur, 2026.

MENDES, Nicolas Satil; CARVALHO, Luciano Gonçalves de. Análise comparativa de implementações padrão de algoritmos de hashing disponibilizadas pelo framework Spring Security. Revista Eletrônica e-Fatec, Garça, v. 16, n. 1, 2026. Disponível em: https://pesquisafatec.com.br/ojs/efatec/pt_BR/article/view/396. Acesso em: _(09/09/2026)_.

---

> Última atualização: _(09/09/2026)_
> Responsável pela documentação: _(Jhonathan Tonello)_
