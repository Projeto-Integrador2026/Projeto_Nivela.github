# Auditoria de Privacidade de Dados e LGPD com Bearer CLI

## 1. Visão Geral
Como parte da esteira DevSecOps do Projeto Nivela, foi integrado o scanner estático de privacidade **Bearer CLI** no GitHub Actions. O objetivo é realizar a verificação automatizada do código-fonte em busca de exposição indevida de PII (Informações Pessoalmente Identificáveis) e garantir a conformidade com a LGPD.

## 2. Cobertura da Análise
* **Scanner Utilizado:** Bearer CLI
* **Foco da Varredura:** Mapeamento de dados sensíveis (PII), sanitização de logs e integridade no tratamento de dados pessoais.
* **Resultado:** Análise estática executada com sucesso no pipeline de CI/CD.

## 3. Evidência de Execução
A varredura foi concluída com sucesso no GitHub Actions, gerando os ficheiros de relatório (`bearer-report.json`) nos artefatos da esteira.