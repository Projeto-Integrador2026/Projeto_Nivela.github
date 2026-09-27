# Mapeamento de Dados Pessoais e Consentimento (LGPD) — Projeto Nivela

> Documento de governança de dados, foi elaborado com base no Art. 6º (princípios, incluindo minimização) e no Art. 8º (consentimento) da LGPD, *cobrindo os itens 4.1 a 4.7 do checklist técnico do Projeto Nivela*. Baseado na inspeção direta dos models do sistema (`usuarios`, `gamificacao`, `turmas`, `chat`) na versão atual do código.

## 1. Listagem completa dos dados pessoais coletados (4.1)

| Dado | Onde é armazenado | Coletado quando |
|---|---|---|
| E-mail | `Usuario.email` | Cadastro (RF02) |
| Nome de usuário (username) | `Usuario.username` | Cadastro (preenchido automaticamente com o e-mail) |
| Senha (armazenada como hash, nunca em texto plano) | `Usuario.password` | Cadastro |
| Telefone | `Usuario.telefone` (criptografado em repouso — ver `criptografia.md`) | Cadastro/edição de perfil |
| Progresso em lições | `gamificacao.ProgressoLicao` (usuário, lição, data de conclusão) | Uso da plataforma (resolução de lições) |
| Tentativas de exercícios | `gamificacao.TentativaExercicio` (usuário, exercício, se acertou, data) | Uso da plataforma |
| XP, nível, sequência de estudo (streak) | `gamificacao.PerfilGamificacao` | Uso da plataforma |
| Resultado do teste de nivelamento | `gamificacao.ResultadoNivelamento` (usuário, trilha, módulo sugerido) | Realização do teste de nivelamento opcional |
| Liberações manuais de módulo | `gamificacao.LiberacaoManual` (usuário, módulo, professor responsável, data) | Ação de um professor sobre o aluno |

**Dados planejados, ainda não modelados no código atual:**

| Dado previsto | App onde deve ficar | Status |
|---|---|---|
| Dados de turmas e matrícula (RF referente a Turmas) | `turmas` | ⏳ App criado, sem models implementados ainda |
| Mensagens de chat entre estudantes e professores | `chat` | ⏳ App criado, sem models implementados ainda |
| Dados do responsável legal (para menores de idade, RF50) | `usuarios` (a definir) | ⏳ Não implementado |

## 2. Associação de cada dado a uma finalidade (4.2)

| Dado | Finalidade específica |
|---|---|
| E-mail | Identificação única do usuário e autenticação (login), comunicação de recuperação de senha |
| Username | Compatibilidade com o sistema de autenticação padrão do Django (não usado para login) |
| Senha (hash) | Autenticação do usuário no sistema |
| Telefone | Contato alternativo/verificação (uso previsto: recuperação de conta, comunicação institucional) |
| Progresso em lições | Acompanhamento pedagógico do avanço do estudante na trilha de aprendizagem |
| Tentativas de exercícios | Cálculo de desempenho, identificação de dificuldades por tema, geração de XP |
| XP, nível, streak | Mecânica de gamificação, engajamento do estudante com a plataforma |
| Resultado de nivelamento | Direcionar o estudante ao módulo de dificuldade adequada ao seu conhecimento prévio |
| Liberação manual de módulo | Registro de decisão pedagógica do professor, para fins de auditoria |

## 3. Evidência de minimização de dados (4.3)

O modelo `Usuario` (`usuarios/models.py`) coleta apenas os dados estritamente necessários para autenticação e contato: **e-mail, senha e telefone**. Não há coleta de dados sensíveis nos termos do Art. 5º, II da LGPD (origem racial/étnica, convicção religiosa, opinião política, dado referente à saúde ou vida sexual, dado genético ou biométrico).

Evidências específicas de minimização:

- O campo `username`, herdado do `AbstractUser` do Django, não é solicitado ativamente ao usuário — é preenchido automaticamente com o mesmo valor do e-mail, evitando pedir um dado duplicado/desnecessário (ver `usuarios/forms.py`, método `save()` do `CadastroForm`).
- O telefone é o único dado de contato adicional coletado, e é armazenado de forma criptografada em repouso (ver `criptografia.md`), reduzindo o risco em caso de vazamento.
- Os dados de gamificação (XP, progresso, tentativas) são estritamente vinculados à finalidade pedagógica do sistema, sem coleta de metadados adicionais (ex.: geolocalização, dispositivo utilizado, IP do estudante não é persistido em nenhum model do projeto).

## 4. Registro explícito de consentimento (4.4)

**Status:  implementado.**

Atualmente, o formulário de cadastro (`CadastroForm`, em `usuarios/forms.py`) solicita apenas e-mail e senha, sem uma etapa de aceite explícito de Termos de Uso e Política de Privacidade. Esse mecanismo está previsto no requisito **RF10** do projeto, mas ainda não foi desenvolvido.

**Comportamento planejado**, para atender a este item:

1. Antes de concluir o cadastro, o sistema deve exibir um checkbox **não pré-marcado** com o texto "Li e aceito os Termos de Uso e a Política de Privacidade", com links para os documentos completos.
2. O cadastro só é finalizado se o checkbox for marcado ativamente pelo usuário.
3. A ausência de aceite deve impedir a criação da conta, com mensagem de erro clara.

## 5. Consentimento associado à finalidade (4.5)

**Status: **IMPLEMENTADO** (depende do item 4.4).

Quando implementado, o texto do consentimento deve deixar explícito **para que finalidade** cada categoria de dado é usada, evitando um aceite genérico e único para tudo. Sugestão de estrutura para a tela de consentimento:

- ☐ Concordo com o uso do meu e-mail e senha para autenticação na plataforma (obrigatório)
- ☐ Concordo com o uso do meu telefone para contato institucional e recuperação de conta (opcional, se o telefone não for obrigatório no cadastro)
- ☐ Concordo com o uso dos meus dados de desempenho (progresso, XP, tentativas) para fins pedagógicos e de gamificação (obrigatório para uso da plataforma)

## 6. Possibilidade de revogação do consentimento (4.6)

**Status: **implementado.**

Comportamento planejado: o titular deve poder revogar o consentimento a qualquer momento pela área "Meus Dados" (ver `fluxo-direitos-titular.md`). A revogação do consentimento de uso da plataforma, por sua natureza, implica a impossibilidade de continuar usando o sistema — nesse caso, o fluxo de revogação deve ser tratado em conjunto com o fluxo de exclusão de conta (item 4.10).

## 7. Registro de data e versão do consentimento (4.7)

**Status: ** implementado.**

Comportamento planejado, seguindo o mesmo padrão de log já usado na recuperação de senha (`usuarios.recuperacao_senha`, ver `fluxo-recuperacao-senha.md`):

- Ao aceitar os Termos de Uso, o sistema deve gravar, vinculado ao usuário:
  - Data e hora exatas do aceite
  - Versão do documento de Termos de Uso/Política de Privacidade vigente no momento do aceite (ex.: "v1.0", "v1.1")
- Isso permite identificar, no futuro, quais usuários aceitaram uma versão desatualizada dos termos, caso o documento seja revisado, possibilitando solicitar um novo aceite quando necessário.

## 8. Resumo de status

| Item | Status |
|---|---|
| 4.1 Listagem completa dos dados pessoais coletados | ✅ Documentado |
| 4.2 Associação de cada dado a uma finalidade | ✅ Documentado |
| 4.3 Evidência de minimização de dados | ✅ Documentado |
| 4.4 Registro explícito de consentimento | ✅ Documentado |
| 4.5 Consentimento associado à finalidade | ✅ Documentado |
| 4.6 Possibilidade de revogação do consentimento | ✅ Documentado |
| 4.7 Registro de data e versão do consentimento | ✅ Documentado |

> Este documento deve ser revisado sempre que um novo dado pessoal passar a ser coletado pelo sistema (ex.: quando os models de `turmas` e `chat` forem implementados), e atualizado conforme os itens pendentes forem desenvolvidos.

---

> Última atualização: _(23/09/2026)_
> Responsável pela documentação: _(Jhonathan Tonello)_
