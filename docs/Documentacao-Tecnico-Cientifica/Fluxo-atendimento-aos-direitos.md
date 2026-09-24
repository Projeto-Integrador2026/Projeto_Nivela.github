# Fluxo de Atendimento aos Direitos  (LGPD) — Projeto Nivela

> Este Documento de processo foi desenvolvido com base no Art. 18 da Lei Geral de Proteção de Dados (LGPD) e nos Requisitos RF11, RF12 e RF50 do Projeto Nivela. Descreve como o sistema deve atender às solicitações dos titulares de dados pessoais (estudantes, professores e responsáveis legais).

## 1. Objetivo

O documento define o fluxo operacional que o sistema Nivela segue (ou deve seguir) para atender às solicitações dos titulares de dados pessoais, garantindo conformidade com os direitos previstos na LGPD, *item 4.11 do checklist técnico do projeto*.

## 2. Direitos do titular cobertos

| Direito (Art. 18, LGPD) | Requisito relacionado | Descrição |
|---|---|---|
| Confirmação da existência de tratamento | RF11 | O titular pode verificar se seus dados estão sendo tratados pelo sistema |
| Acesso aos dados | RF11 | O titular pode consultar todos os dados pessoais armazenados sobre ele |
| Correção de dados incompletos, inexatos ou desatualizados | RF11 | O titular pode solicitar/realizar a correção de seus próprios dados |
| Portabilidade dos dados | RF12 | O titular pode exportar seus dados em formato estruturado (ex.: JSON) |
| Eliminação dos dados tratados com consentimento | RF12 | O titular pode solicitar a exclusão de sua conta e dados associados |
| Revogação do consentimento | RF10 | O titular pode revogar o consentimento dado previamente |
| Informação sobre uso compartilhado de dados | RF11 | O titular pode ser informado sobre com quem seus dados são compartilhados, se aplicável |

## 3. Fluxo geral de atendimento

```
1. Titular autenticado acessa a área "Meus Dados" no perfil do sistema
2. Sistema identifica o usuário exclusivamente via sessão ativa
   (nenhuma solicitação é aceita sem autenticação prévia)
3. Titular escolhe a ação desejada: consultar, corrigir, exportar ou excluir
4. Sistema executa a ação correspondente (ver seções 3.1 a 3.4)
5. Ação é registrada em log de auditoria (quem, quando, o que foi solicitado)
6. Sistema confirma a conclusão da solicitação ao titular
```

### 3.1 Consulta de dados (RF11)

1. Titular acessa "Meus Dados"
2. Sistema exibe, em tela, todos os dados pessoais vinculados à conta (nome, e-mail, telefone, turmas, histórico de gamificação, mensagens de chat associadas)
3. Nenhuma informação de outro usuário é exibida, mesmo que relacionada (ex.: mensagens de terceiros em um chat compartilhado são omitidas ou anonimizadas)

### 3.2 Correção de dados (RF11)

1. Titular acessa "Meus Dados" → "Editar"
2. Campos editáveis (nome, telefone, etc.) ficam disponíveis para atualização direta pelo próprio usuário
3. Alterações são salvas imediatamente, sem necessidade de aprovação manual, exceto o e-mail (usado como identificador de login), que exige confirmação adicional

### 3.3 Exportação/portabilidade de dados (RF12)

1. Titular acessa "Meus Dados" → "Exportar meus dados"
2. Sistema identifica o usuário via sessão ativa
3. Sistema gera um arquivo estruturado (formato JSON) contendo todos os dados pessoais vinculados àquele usuário
4. Ação é registrada em log (usuário, data/hora, tipo de solicitação)
5. Arquivo é disponibilizado para download imediato

### 3.4 Eliminação de dados / exclusão de conta (RF12)

1. O Titular acessa "Meus Dados" → "Excluir minha conta"
2. O Sistema solicita confirmação explícita (ex.: reautenticação de senha) antes de prosseguir, para evitar exclusões acidentais
3. O Sistema executa a exclusão ou anonimização dos dados pessoais, conforme a política de retenção vigente (RNF09)
4. Dados que precisem ser mantidos por obrigação legal (ex.: registros acadêmicos exigidos por instituição de ensino) são anonimizados, não excluídos, e essa exceção é informada ao titular
5. Ação é registrada em log de auditoria

## 4. Prazo de atendimento

A LGPD não estabelece um prazo único e obrigatório para todas as solicitações, mas recomenda resposta em prazo razoável. O Projeto Nivela adota como referência interna:

- **Confirmação de existência de tratamento e acesso aos dados:** imediato (funcionalidade de autoatendimento, sem necessidade de intervenção manual)
- **Correção de dados:** imediato (autoatendimento)
- **Exportação de dados:** imediato (autoatendimento)
- **Exclusão de conta:** imediato para o usuário final; eventual retenção de dados por obrigação legal é comunicada no momento da solicitação

## 5. Verificação de identidade do solicitante

Todas as solicitações de direitos do titular exigem autenticação ativa no sistema (sessão válida), reaproveitando os mecanismos de segurança já implementados no Requisito 1 (hash de senha, 2FA obrigatório). Isso garante que apenas o próprio titular — ou o responsável legal, no caso de menores de idade — consiga acessar, alterar ou excluir os dados em questão.

### 5.1 Caso especial: estudantes menores de idade (RF50)

Quando o titular dos dados é um estudante menor de idade, solicitações relacionadas a consentimento, correção ou exclusão de dados devem ser mediadas pelo responsável legal cadastrado, conforme já previsto no requisito RF50 (consentimento obrigatório do responsável antes do cadastro). O fluxo de atendimento aos direitos, nesses casos, segue o mesmo processo descrito acima, mas a autenticação e a ação são realizadas pela conta do responsável, não pela do menor.

## 6. Registro e auditoria das solicitações

Toda solicitação relacionada aos direitos do titular (consulta, correção, exportação ou exclusão) deve ser registrada em log, seguindo o mesmo padrão já adotado para a recuperação de senha (ver `fluxo-recuperacao-senha.md`), contendo:

- Identificação do usuário solicitante
- Tipo de solicitação realizada
- Data e hora da solicitação
- Resultado (sucesso ou falha, com motivo)



---

> Última atualização: _(20/09/2026)_
> Responsável pela documentação: _(Jhonathan Tonello)_
