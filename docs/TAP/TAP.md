TERMO DE ABERTURA DO PROJETO (TAP) — NIVELA

1. Identificação do Projeto
•	Nome do projeto: Nivela
•	Tipo de projeto: Desenvolvimento de Software Educacional
•	Área: Educação e Tecnologia
•	Plataforma: Web
•	Natureza: Projeto Integrador — Engenharia de Software
•	Equipe do projeto: Beatriz, Jhonathan e Vinicius
•	Professor responsável: Fabiano M.

2. Justificativa do Projeto
Em uma mesma turma, os estudantes apresentam diferentes níveis de conhecimento, dificuldades e ritmos de aprendizagem. Essa divergência dificulta a formação de equipes equilibradas, o acompanhamento individualizado e a detecção tempestiva de barreiras de aprendizado.
Atualmente, professores e estudantes recorrem a um ecossistema fragmentado de ferramentas para comunicação, atividades, conteúdos e gestão. Diante desse cenário, surge a proposta do Nivela, uma plataforma web que busca centralizar recursos de aprendizagem e utilizar o nivelamento diagnóstico dos estudantes como base principal para organizar conteúdos, atividades e grupos de estudo colaborativos.

3. Definição do Problema
Problema Central: Como facilitar o acompanhamento da evolução dos estudantes e a formação de grupos de aprendizagem produtivos quando os alunos de uma mesma turma possuem níveis de conhecimento distintos?
Hoje, a identificação dessas diferenças depende quase exclusivamente da percepção empírica do professor ou de avaliações periódicas. Para detalhar o cenário, foram identificadas 7 dores principais:
1.	Falta de diagnóstico inicial estruturado: O professor tem dificuldade em identificar o nível real da turma para conduzir o conteúdo de forma que atenda tanto quem já domina o assunto quanto quem tem defasagens básicas.
2.	Ausência de ambiente para revisão rápida: Faltam espaços específicos para microaprendizagem e revisão de conceitos fora da sala de aula.
3.	Desconexão entre teoria e prática: Dificuldade dos alunos em aplicar conceitos teóricos em exercícios e situações práticas.
4.	Gargalos na comunicação: Falta de um canal de suporte integrado e eficiente entre alunos e professores.
5.	Fragmentação de ferramentas: O uso excessivo de múltiplas plataformas (Teams, Duolingo, Kahoot, Classroom, GitHub, IAs, etc.) desorganiza o estudo do aluno e o acompanhamento do professor.
6.	Desequilíbrio na formação de equipes: Dificuldade em montar grupos de trabalho onde os integrantes se complementem, devido à ausência de dados claros sobre o nível de cada um.
7.	Inviabilidade da monitoria descentralizada: Dificuldade logística para organizar encontros de monitoria presencial entre os próprios estudantes de forma supervisionada.

4. Objetivo Geral
Desenvolver uma plataforma web educacional focada no diagnóstico e nivelamento contínuo dos estudantes, que centralize trilhas de aprendizagem, promova a formação inteligente de grupos de estudo e viabilize a monitoria colaborativa entre alunos, garantindo ao professor uma visão unificada e analítica da evolução da turma.
5. Objetivos Específicos
•	Mapear perfis: Implementar um módulo de diagnóstico inicial para classificar o nível de conhecimento técnico/teórico dos estudantes.
•	Estruturar o ensino: Desenvolver trilhas de microaprendizagem e repositórios de atividades práticas integradas.
•	Engajar usuários: Aplicar estratégias de gamificação para estimular a retenção e o uso contínuo da ferramenta.
•	Potencializar a colaboração: Criar um algoritmo ou lógica que facilite a formação de grupos de estudo equilibrados com base nos níveis identificados.
•	Viabilizar monitorias: Desenvolver um sistema que conecte estudantes com maior facilidade a colegas que necessitam de reforço, sob a supervisão do docente.
•	Unificar a experiência: Centralizar comunicação, gestão de conteúdo e dashboard de métricas em um único ecossistema web.
6. Descrição da Solução
O Nivela será concebido como um ambiente virtual de aprendizagem inovador. A jornada do usuário começará com um diagnóstico de nivelamento que alimentará o sistema com dados sobre suas proficiências. A partir desses dados, a plataforma recomendará trilhas de conteúdos, exercícios e microaulas adaptadas à necessidade de cada perfil.
O grande diferencial será a utilização destes dados para conectar pessoas: o sistema sugerirá a formação de equipes onde os conhecimentos se complementam e permitirá que alunos com alto desempenho se voluntariem (ou sejam convidados) a realizar monitorias na própria plataforma, sempre amparados e acompanhados pelo professor responsável, que terá dashboards completos para identificar gargalos e medir a evolução da turma.

7. Principais Funcionalidades
Para Estudantes:
•	Cadastro e autenticação segura;
•	Testes de diagnóstico e nivelamento inicial;
•	Acesso a trilhas de microaprendizagem e exercícios práticos;
•	Dashboard pessoal de progresso e sistema de pontuação (gamificação);
•	Comunicação em chat integrado com professores e colegas;
•	Solicitação e prestação de monitoria;
•	Participação em grupos de estudo sugeridos.
Para Professores:
•	Gestão integral de turmas e criação de atividades/trilhas;
•	Dashboard analítico com resultados dos diagnósticos e evolução da turma;
•	Identificação rápida de dificuldades recorrentes;
•	Supervisão e mediação das monitorias e dos grupos formados.
Para Administradores:
•	Gerenciamento global de usuários, perfis (RBAC) e permissões;
•	Manutenção do sistema, infraestrutura e parametrizações gerais.

8. Público-Alvo
Na versão inicial (MVP), o foco será em turmas (especialmente de ensino técnico ou superior) que sabidamente apresentam grande disparidade de níveis de conhecimento inicial.
•	Usuários diretos: Estudantes (Ensino Fundamental, Médio, Técnico e Superior) e Professores.
•	Clientes (potenciais): Instituições de ensino público ou privado.

9. Escopo do Projeto
Dentro do Escopo (MVP):
•	Plataforma Web responsiva;
•	Sistema de Autenticação e Controle de Acesso (Perfis);
•	Módulos de Nivelamento, Trilhas de Aprendizagem e Atividades;
•	Módulo de Grupos e Monitoria entre pares;
•	Dashboard do Professor e Chat básico;
•	Adequação às premissas da LGPD (Segurança de dados).
Fora do Escopo Inicial:
•	Aplicativo mobile nativo (iOS/Android);
•	Integração via API com sistemas acadêmicos corporativos de terceiros (ex: Totvs, Moodle);
•	Inteligência Artificial generativa nativa para criar conteúdo automaticamente;
•	Módulos financeiros ou de comercialização (pagamentos).

10. Requisitos de Segurança e LGPD
O desenvolvimento adotará a abordagem de Privacy by Design. Por tratar dados de menores e desempenho escolar, o sistema garantirá:
•	Controle de Acesso: Baseado em funções (RBAC - Role-Based Access Control).
•	Criptografia: Dados sensíveis em repouso e em trânsito (HTTPS/TLS).
•	Princípios da LGPD: Anonimização de dados para análises estatísticas, consentimento explícito no cadastro e aplicação estrita dos princípios de Finalidade, Adequação e Necessidade.

11. Premissas
•	Os usuários finais possuirão dispositivos com acesso regular à internet.
•	Haverá engajamento do corpo docente para alimentar a plataforma e analisar os dados.
•	O desenvolvimento inicial buscará a entrega de um Protótipo Funcional/MVP para validação.
•	A equipe de desenvolvimento utilizará ferramentas e frameworks gratuitos ou open-source adequados à realidade acadêmica.

12. Restrições
•	Tempo: O cronograma é estritamente limitado ao prazo estipulado pelo calendário do Projeto Integrador.
•	Recursos: Orçamento financeiro nulo ou extremamente limitado, restringindo uso de serviços em nuvem pagos.
•	Equipe: Esforço limitado às horas disponíveis dos 3 integrantes do grupo.

13. Principais Stakeholders
Stakeholder	Interesse no projeto
Estudantes	Aprender, acompanhar sua evolução e colaborar em grupo.
Professores	Otimizar tempo, acompanhar desempenho e focar nas dificuldades reais.
Instituições de Ensino	Modernizar metodologias, unificar plataformas e reter alunos.
Administradores	Estabilidade, segurança e fácil gestão do sistema.
Equipe do Projeto	Entregar software de qualidade, aplicar conceitos da engenharia e ser aprovado na disciplina.
Responsáveis (Pais)	Acompanhamento estruturado e segurança digital para os menores.

14. Entregas Principais
1.	Documentação de Requisitos e Regras de Negócio;
2.	Modelagem de Software (UML) e Banco de Dados (DER);
3.	Protótipos navegáveis de UI/UX (Figma ou similar);
4.	Módulo Base: Autenticação e Gestão de Perfis;
5.	Módulo de Diagnóstico e Nivelamento;
6.	Módulo Pedagógico (Trilhas, Atividades e Gamificação);
7.	Módulo de Integração (Grupos, Monitoria e Chat);
8.	Dashboard Analítico (Visão Professor);
9.	Bateria de Testes Funcionais e de Segurança;
10.	Entrega Final: MVP da Plataforma "Nivela" operante e documentada.
15. Critérios de Sucesso
•	Capacidade comprovada do sistema em realizar testes e classificar perfis.
•	Fluxo funcional validado entre o nivelamento do aluno, o acesso à trilha correta e a formação inteligente de grupos.
•	Interface amigável atestada por usuários beta (testes de usabilidade).
•	Código-fonte documentado e segurança de acesso efetiva.
•	Aprovação técnica e acadêmica pelo professor responsável pela disciplina.

16. Riscos Iniciais
Risco	Impacto	Estratégia de Mitigação
Prazo insuficiente para desenvolvimento	Alto	Priorizar o escopo do MVP estritamente; utilizar metodologias ágeis (Scrum/Kanban).
Complexidade da lógica de formação de grupos	Alto	Criar algoritmos simplificados no MVP antes de tentar regras muito robustas.
Vazamento ou mau tratamento de dados	Alto	Definir arquitetura segura e seguir LGPD desde a linha 1 de código.
Baixa adesão por atrito tecnológico	Médio	Focar massivamente em UX/UI amigável e investir nos gatilhos de gamificação.
Curva de aprendizado técnica da equipe	Médio	Realizar provas de conceito (PoC) rápidas das tecnologias escolhidas antes de codificar o sistema final.

17. Visão do Produto
O Nivela pretende funcionar como um hub central de aprendizagem. A inovação está em subverter a lógica das plataformas atuais: o nivelamento não servirá apenas para "dar uma nota" ao estudante, mas será o motor principal que direcionará o algoritmo do sistema para personalizar conteúdos, sugerir parcerias de estudo e otimizar a atenção do professor, transformando a disparidade de conhecimento de um problema em uma oportunidade de colaboração mútua.
18. Aprovação do Projeto
A aprovação deste Termo de Abertura representa o início formal do desenvolvimento do projeto Nivela, autorizando a equipe responsável a iniciar as etapas de engenharia de requisitos, modelagem, desenvolvimento e validação.
Data: //________
Professor responsável: ______________________________
Representante da equipe: ____________________________
Assinatura: _________________________________________
