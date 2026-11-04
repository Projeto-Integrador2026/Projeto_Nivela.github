# Evidências do Pipeline DevSecOps - Análise DAST (OWASP ZAP)

Este repositório contém a documentação visual e técnica da execução da etapa de **Análise Dinâmica de Segurança de Aplicações (DAST)** no pipeline de CI/CD do Projeto Nivela, utilizando a ferramenta **OWASP ZAP (Zed Attack Proxy)**.

O objetivo desta etapa é validar a segurança da aplicação em tempo de execução, realizando varreduras ativas e passivas em busca de vulnerabilidades de infraestrutura, cabeçalhos de segurança ausentes, falhas de exposição de dados e configurações incorretas no ambiente de staging/teste.

---

## 📸 Detalhamento das Evidências

Abaixo está a descrição e a comprovação técnica referente a cada imagem armazenada nesta pasta:

### 1. `01-execucao-main-verde.jpg`
* **Descrição:** Execução bem-sucedida do workflow principal de CI/CD na branch `main`.
* **Comprovação:** Mostra todos os jobs anteriores (build, lint e testes unitários/cobertura) finalizados com status verde (sucesso), garantindo que a base de código está estável antes do acionamento dos testes dinâmicos.

### 2. `02-build-e-subida-da-app_a.jpg`
* **Descrição:** Inicialização do container e preparação do ambiente da aplicação para varredura.
* **Comprovação:** Registra a subida dos serviços via Docker/Compose e a alocação da porta local de execução, confirmando que o endpoint da aplicação ficou online e pronto para receber requisições do scanner.

### 3. `02-build-e-subida-da-app_b.jpg`
* **Descrição:** Logs da aplicação e teste de conectividade (healthcheck).
* **Comprovação:** Demonstra que as variáveis de ambiente foram carregadas corretamente e que a aplicação respondeu com status HTTP `200 OK` na rota raiz/saúde antes do início dos testes do ZAP.

### 4. `02-build-e-subida-da-app_c.jpg`
* **Descrição:** Configuração dos parâmetros de mascaramento de segredos no log do runner.
* **Comprovação:** Exibe a criação de credenciais efêmeras de teste utilizando `::add-mask::`, garantindo que NENHUMA chave de criptografia ou segredo (`SECRET_KEY`, `FIELD_ENCRYPTION_KEY`) seja exposto em texto claro nos logs do GitHub Actions.

### 5. `03-zap-alvo-localhost_a.jpg`
* **Descrição:** Início da varredura ativa/passiva do OWASP ZAP direcionada ao alvo.
* **Comprovação:** Confirma o apontamento do container do OWASP ZAP para a URL alvo (`http://localhost:8000`), exibindo os parâmetros de entrada da ferramenta e a spidersurvey crawling na aplicação.

### 6. `03-zap-resumo_b.jpg`
* **Descrição:** Sumário da varredura executada pelo OWASP ZAP no terminal/runner.
* **Comprovação:** Exibe a contagem total de requisições disparadas, quantidade de alertas gerados divididos por severidade (Alto, Médio, Baixo, Informacional) e a conclusão da análise sem interrupções de conexão.

### 7. `04-relatorio-zap-alerta_b.jpg`
* **Descrição:** Detalhamento dos alertas de segurança identificados no relatório de saída.
* **Comprovação:** Apresenta a descrição técnica dos alertas detectados (ex.: ausência de cabeçalhos HTTP como `X-Content-Type-Options` ou `Strict-Transport-Security`), indicando a URL afetada e o vetor da requisição.

### 8. `04-relatorio-zap-resumo_a.jpg`
* **Descrição:** Artefato do relatório consolidado gerado pelo ZAP (`HTML`/`JSON`).
* **Comprovação:** Demonstra a gravação do arquivo de relatório final no diretório de saída e sua disponibilização para upload nos artefatos do workflow do GitHub Actions.

### 9. `05-quality-gate-log_a.jpg`
* **Descrição:** Execução das regras de validação do Quality Gate de segurança.
* **Comprovação:** Mostra o script de verificação analisando o número de alertas críticos e altos em comparação aos limites tolerados pela política de segurança DevSecOps do projeto.

### 10. `05-regras-fail_b.jpg`
* **Descrição:** Validação final e aprovação/bloqueio conforme a política de segurança.
* **Comprovação:** Registra o comportamento do pipeline diante dos achados de segurança, comprovando que a esteira falha adequadamente se vulnerabilidades de alta gravidade forem detectadas (ou passa com aviso caso apenas alertas baixos/médios conhecidos estejam presentes).