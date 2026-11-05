# Testes Dinâmicos de Segurança (DAST) com OWASP ZAP

## 1. Visão Geral
Como parte da esteira DevSecOps do Projeto Nivela, foi implementada a análise dinâmica de segurança (DAST) automatizada via GitHub Actions. O scanner OWASP ZAP realiza varreduras ativas e passivas na aplicação em execução para identificar potenciais vulnerabilidades.

## 2. Resultado da Varredura
A execução automatizada do pipeline obteve aprovação no *Quality Gate*, não identificando vulnerabilidades críticas.

### Resumo dos Alertas:
* **Crítico / Alto (High):** 0
* **Médio (Medium):** 6
* **Baixo (Low):** 6
* **Informativo (Info):** 12
* **Total:** 24 alertas, nenhum bloqueante
* **Falsos positivos marcados:** 0

## 3. Evidência de Execução

![Relatório OWASP ZAP](../Evidencias/dast/relatorio-owasp-zap.jpg)
*Figura 1: Relatório de varredura dinâmica gerado pelo OWASP ZAP.*

## 4. Análise Técnica e Próximos Passos
Os alertas de nível médio identificados referem-se maioritariamente à ausência de cabeçalhos de segurança HTTP (como *Content Security Policy - CSP*). Estas melhorias foram documentadas para implementação nas próximas iterações.

## 5. Limitações

- **Cobertura:** o ZAP varre a aplicação sem autenticação, então só percorre as páginas públicas (cadastro, login, recuperação de senha e arquivos estáticos). As áreas internas exigem login e verificação em duas etapas (2FA) e não são varridas por este job. Falhas nessas áreas não são detectadas por ele.
- **Quality gate:** o build é bloqueado por alertas de severidade explorável definidos em `.zap/rules.tsv` (XSS refletido, persistente e DOM; SQL Injection e variantes; Server Side Code Injection; Remote OS Command Injection; Path Traversal; Remote File Inclusion; CRLF Injection). Regras que não constam no arquivo, como as de cabeçalhos HTTP (por exemplo, Content-Security-Policy ausente), ficam como **aviso** e não quebram o build. Na última execução: 0 alertas bloqueantes e 24 avisos.
- **HSTS:** a regra 10035 (Strict-Transport-Security) é ignorada no CI, porque a aplicação roda em HTTP puro no runner, sem TLS, e o cabeçalho só é emitido em HTTPS. Em produção ele é verificado (ver `docs/Evidencias/criptografia-comunicacao-segura`).
- **Ambiente:** a varredura roda contra a aplicação em `localhost`, com banco de teste e `DEBUG=False`, e não contra o ambiente de produção.