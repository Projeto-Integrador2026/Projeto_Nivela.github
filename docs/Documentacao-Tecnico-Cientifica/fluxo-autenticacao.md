# Fluxo de Autenticação — Projeto Nivela

## Fluxo de Login

1. Usuário acessa a tela de login e informa e-mail e senha
2. Sistema verifica se o e-mail existe na base
3. Sistema verifica se a conta não está bloqueada por tentativas excessivas (RNF15)
4. Sistema compara o hash da senha informada com o hash armazenado, usando o salt do usuário (RNF10, RNF12)
5. Se a senha estiver correta:
   - Se o 2FA estiver ativo (RF07, desejável) → sistema solicita o segundo fator de autenticação (RF08)
   - Se o 2FA não estiver ativo → segue direto para a criação da sessão
6. Sistema cria a sessão do usuário, com tempo de expiração definido (RNF14)
7. Sistema registra o evento de login no log de auditoria (RNF16)

## Casos de erro

| Situação | Comportamento do sistema |
|---|---|
| Senha incorreta | Incrementa o contador de tentativas; após N tentativas, aplica bloqueio temporário ou atraso progressivo (RNF15) |
| Conta inativa/excluída | Acesso negado, sem detalhar o motivo (evita enumeração de contas) |
| Código de 2FA incorreto | Retorna à etapa de inserção do código, sem criar a sessão |
| Tentativa após bloqueio temporário | Acesso negado até o tempo de bloqueio expirar |

## Encerramento de sessão (logout)

1. Usuário solicita logout
2. Sistema invalida a sessão ativa (RF09)
3. Sistema registra o evento de logout no log de auditoria (RNF16)

---

> Última atualização: _(29/08/2026)_
> Responsável pela documentação: _(Jhonathan Tonello)_
