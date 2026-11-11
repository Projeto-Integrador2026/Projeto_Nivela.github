# Checklist de Requisitos — Projeto Nivela

Checklist técnico do projeto, cobrindo autenticação, segurança, LGPD, documentação e entrega. Marque `[x]` conforme os itens forem concluídos.

## 1. Autenticação e Gestão de Credenciais

- [x] 1.1 Uso de hash criptográfico seguro para senhas (Argon2, bcrypt ou PBKDF2)
- [x] 1.2 Parâmetros de custo do hash configurados e justificados
- [x] 1.3 Uso de salt criptográfico único por usuário
- [x] 1.4 Armazenamento correto do hash + salt
- [x] 1.5 Autenticação de dois fatores (2FA) implementada
- [x] 1.6 Validação do 2FA após autenticação primária
- [x] 1.7 Fluxo de autenticação documentado
- [X] 1.8 Evidências funcionais (prints, logs ou testes)
- [x] 1.9 Sessões com tempo de expiração
- [x] 1.10 Invalidação de sessão no logout
- [x] 1.11 Proteção contra força bruta (rate limit, bloqueio, atraso)
- [x] 1.12 Justificativas técnicas documentadas

## 2. Recuperação de Senha

- [X] 2.1 Funcionalidade de recuperação de senha implementada
- [X] 2.2 Token criptograficamente seguro
- [X] 2.3 Token com tempo de expiração
- [X] 2.4 Token invalidado após uso
- [X] 2.5 Falha correta para token expirado
- [X] 2.6 Registro de solicitação de recuperação em log
- [X] 2.7 Registro de sucesso/falha do processo

> **Nota sobre a Seção 2:** os itens acima estão implementados no código e cobertos por teste. Em produção, porém, o plano gratuito do Render bloqueia o envio de e-mail por SMTP, então o link de redefinição não chega ao usuário. A limitação é de infraestrutura e está registrada na Seção 9 (DEC-01 e DEC-02).

## 3. Criptografia e Comunicação Segura

- [X] 3.1 Comunicação protegida por TLS/HTTPS
- [X] 3.2 Bloqueio de conexões não seguras
- [X] 3.3 Evidência de tráfego cifrado
- [X] 3.4 Dados sensíveis criptografados em repouso
- [X] 3.5 Uso de algoritmo criptográfico adequado (ex.: AES)
- [X] 3.6 Chaves criptográficas protegidas
- [x] 3.7 Estratégia de criptografia documentada
- [x] 3.8 Justificativa técnica das escolhas

## 4. Conformidade com a LGPD

- [x] 4.1 Listagem completa dos dados pessoais coletados
- [x] 4.2 Associação de cada dado a uma finalidade
- [x] 4.3 Evidência de minimização de dados
- [x] 4.4 Registro explícito de consentimento
- [x] 4.5 Consentimento associado à finalidade
- [x] 4.6 Possibilidade de revogação do consentimento
- [x] 4.7 Registro de data e versão do consentimento
- [x] 4.8 Funcionalidade de consulta aos dados do titular
- [x] 4.9 Funcionalidade de exportação dos dados
- [x] 4.10 Funcionalidade de exclusão dos dados pessoais
- [x] 4.11 Fluxo de atendimento aos direitos documentado

## 5. Auditoria e Logs

- [X] 5.1 Logs de autenticação registrados
- [X] 5.2 Logs de falhas e 2FA registrados
- [X] 5.3 Proteção contra alteração dos logs
- [X] 5.4 Exemplo de análise de logs apresentado

## 6. Documentação Técnico-Científica

- [x] 6.1 Documento de visão geral do sistema
- [x] 6.2 Diagrama de arquitetura
- [x] 6.3 Fluxos de autenticação e dados documentados
- [x] 6.4 Gestão de credenciais documentada
- [x] 6.5 Uso de criptografia documentado
- [x] 6.6 Identificação dos ativos do sistema
- [x] 6.7 Identificação de ameaças e vulnerabilidades
- [x] 6.8 Associação risco × contramedida
- [ ] 6.9 Testes de segurança realizados
- [ ] 6.10 Resultados dos testes documentados
- [x] 6.11 Uso de artigos científicos e/ou normas técnicas
- [x] 6.12 Referências normalizadas

## 7. Resumo Científico

- [x] 7.1 Resumo entre 200 e 300 palavras
- [ ] 7.2 Objetivo claramente definido
- [ ] 7.3 Metodologia técnica descrita
- [x] 7.4 Mecanismos de segurança apresentados
- [x] 7.5 Conformidade com a LGPD explicitada
- [ ] 7.6 Terminologia técnica adequada
- [ ] 7.7 Qualidade textual e científica

## 8. Pôster Científico e Apresentação

- [ ] 8.1 Estrutura científica do pôster
- [ ] 8.2 Arquitetura e fluxos representados visualmente
- [ ] 8.3 Evidência de conformidade com LGPD
- [ ] 8.4 Qualidade técnica dos diagramas
- [ ] 8.5 Coerência com o sistema entregue
- [ ] 8.6 Domínio técnico na apresentação
- [ ] 8.7 Capacidade de resposta às perguntas

## 9. Decisões de Projeto e Riscos Aceitos

Decisões tomadas conscientemente pelo grupo que reduzem uma proteção para garantir o funcionamento do sistema. Cada uma indica o motivo, o risco residual e o plano de reversão.

| ID | Decisão | Motivo | Risco residual | Mitigações existentes | Revisão prevista |
|---|---|---|---|---|---|
| DEC-01 (achado A-06) | O e-mail informado no cadastro **não é verificado**: a conta nasce ativa e o cadastro não envia e-mail de ativação. | O plano gratuito do Render bloqueia as portas SMTP de saída (25, 465 e 587) desde 26/09/2025. O e-mail de ativação nunca chegava e as contas ficavam inativas, impedindo o login. | **Médio.** Alguém pode cadastrar o e-mail de outra pessoa. Como o 2FA é configurado no primeiro login, quem cadastrar primeiro também registra o autenticador da conta. | 2FA obrigatório (TOTP); aceite de Termos de Uso registrado com data e versão; senha com PBKDF2; bloqueio por tentativas (django-axes); resposta idêntica para e-mail já cadastrado (A-04). | Reativar a verificação ao migrar para plano pago ou para um serviço de e-mail por API HTTP. |
| DEC-02 | A recuperação de senha por e-mail **não entrega o link em produção**. | Mesma causa da DEC-01: SMTP bloqueado no Render Free. | **Baixo a médio.** O usuário que esquecer a senha depende de redefinição manual pelos administradores. | Fluxo implementado e testado no código (itens 2.1 a 2.7). Em desenvolvimento o e-mail é exibido no console. | Resolvida junto com a DEC-01. |

---

> Última atualização: _(18/10/2026)_
> Responsável pela documentação: _(Jhonathan Tonello)_
