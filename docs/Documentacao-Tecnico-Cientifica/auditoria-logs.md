# Auditoria e Logs — Projeto Nivela

> Documenta os mecanismos de auditoria implementados (Requisito 5) e apresenta um exemplo prático de análise de log, usado para investigar um incidente de autenticação.

## 1. Visão geral

O sistema mantém dois arquivos de log, gerados automaticamente via signals do Django (sem necessidade de alterar as views):

| Arquivo | Logger | O que registra |
|---|---|---|
| `logs/autenticacao.log` | `usuarios.autenticacao` | Login, logout, falha de senha, falha de código 2FA e validação de 2FA (itens 5.1 e 5.2) |
| `logs/recuperacao_senha.log` | `usuarios.recuperacao_senha` | Solicitação e resultado da recuperação de senha (itens 2.6 e 2.7) |

Cada linha registra data/hora, nível (`INFO` para eventos normais, `WARNING` para falhas), o e-mail do usuário mascarado (ex.: `b***@gmail.com`, mesma técnica de minimização usada no Requisito 4 — LGPD) e o IP de origem, quando disponível.

Desde o item 5.3, cada linha também carrega um hash SHA-256 encadeado com a linha anterior (`| hash=...`), verificável com:

```
python manage.py verificar_logs logs/autenticacao.log
```

## 2. Exemplo de análise — sequência de login de um único usuário

Trecho real de `logs/autenticacao.log`, coletado durante os testes do item 5.2 (hashes abreviados aqui só para facilitar a leitura; os valores completos ficam no arquivo e nas evidências em `docs/Evidencias/auditoria-logs/`):

```
2026-09-27 10:32:29 WARNING FALHA no login - usuario: b***@gmail.com - IP: 127.0.0.1 | hash=7e1a...
2026-09-27 10:32:57 WARNING FALHA no codigo 2FA - usuario: b***@gmail.com | hash=9c4f...
2026-09-27 10:33:22 INFO LOGIN bem-sucedido - usuario: b***@gmail.com - IP: 127.0.0.1 | hash=faf7...
2026-09-27 10:33:22 INFO 2FA validado com sucesso - usuario: b***@gmail.com - dispositivo: TOTPDevice - IP: 127.0.0.1 | hash=8135...
```

**Leitura linha a linha:**

1. **10:32:29 — FALHA no login**: alguém tentou entrar com o e-mail `b***@gmail.com`, mas errou a senha. O IP fica registrado (`127.0.0.1`), permitindo cruzar com outras tentativas vindas do mesmo endereço.
2. **10:32:57 — FALHA no código 2FA**: 28 segundos depois, alguém passou pela etapa de senha (senha certa dessa vez) mas errou o código de 6 dígitos do autenticador. Esse sinal não traz o IP (limitação da biblioteca `django_otp`), só confirma qual conta foi alvo.
3. **10:33:22 — LOGIN bem-sucedido + 2FA validado com sucesso**: na tentativa seguinte, senha e código corretos — acesso concluído.

**O que essa sequência indica:** alguém tentou acessar a conta três vezes em menos de um minuto, errando primeiro a senha e depois o código 2FA, até acertar os dois. Isoladamente, isso é compatível com o próprio dono da conta errando a digitação. Mas o mesmo padrão, vindo de um **IP desconhecido** ou **fora do horário normal de uso**, seria um indício de tentativa de acesso indevido (alguém que descobriu a senha, mas não tem o dispositivo de 2FA) e justificaria: (a) cruzar com o painel do `django-axes` (que já registra e bloqueia por username+IP após 5 tentativas, item 1.11), (b) notificar o titular da conta, e (c) considerar forçar a troca de senha.

**Verificação de integridade antes de confiar na análise:** qualquer investigação só faz sentido se o log não tiver sido adulterado. Por isso, o primeiro passo de qualquer análise é rodar `python manage.py verificar_logs logs/autenticacao.log` e confirmar `OK` antes de tirar conclusões — evidências desse teste (incluindo uma adulteração proposital detectada com sucesso) estão em `docs/Evidencias/auditoria-logs/`.

## 3. Limitações conhecidas

- O log de falha de 2FA (`otp_verification_failed`) não inclui o IP de origem, por não receber o objeto `request` do Django — limitação da própria biblioteca `django_otp`, documentada em `usuarios/signals.py`.
- Os arquivos de log ficam no disco local do servidor (`logs/`) e, no plano gratuito do Render, esse disco é efêmero: os logs não sobrevivem a um redeploy. Para uso em produção real, o próximo passo seria enviar os logs para um serviço externo de armazenamento persistente (ex.: um bucket de logs ou um serviço de observabilidade).