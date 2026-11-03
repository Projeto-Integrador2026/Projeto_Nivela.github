# Segurança da Cadeia de Suprimentos (Supply Chain Security) e SBOM

## 1. Visão Geral
Como parte da esteira DevSecOps do Projeto Nivela, foi implementada a auditoria automatizada de dependências de software e análise da cadeia de suprimentos (*Supply Chain Security*) via GitHub Actions.

## 2. Ferramentas Utilizadas
* **pip-audit:** Auditoria estática de pacotes Python instalados, verificando vulnerabilidades conhecidas em bases de dados públicas (CVEs).
* **Trivy (Aqua Security):** Varredura de segurança do sistema de ficheiros e geração da lista de componentes do software (*Software Bill of Materials - SBOM*).

## 3. Evidência de Execução
A auditoria foi executada com sucesso no pipeline de CI/CD, gerando o relatório `trivy-report.txt` com a relação completa de dependências e respetivas análises de segurança.