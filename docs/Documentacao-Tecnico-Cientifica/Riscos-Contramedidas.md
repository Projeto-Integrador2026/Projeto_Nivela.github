# Associação Risco × Contramedida — Projeto Nivela

> Documento de análise de segurança, associando cada risco/ameaça identificado à contramedida correspondente no sistema. Elaborado com base nos documentos já produzidos (`justificativas-tecnicas.md`, `fluxo-autenticacao.md`, `criptografia.md`) e nos Requisitos v3.

## 1. Riscos com contramedida já implementada

| Risco / Ameaça | Contramedida | Status | Documentado em |
|---|---|---|---|
| Ataque de força bruta no login (tentativas repetidas de adivinhar senha) | django-axes: bloqueio da conta após 5 tentativas falhas, cooloff de 1 hora | ✅ Implementado | `justificativas-tecnicas.md` |
| Vazamento de senha em texto plano (banco comprometido) | Hash PBKDF2 com salt único por usuário, nunca armazenando senha em texto plano | ✅ Implementado | `justificativas-tecnicas.md` |
| Acesso indevido usando apenas e-mail/senha vazados | 2FA obrigatório para todos os perfis, via middleware | ✅ Implementado | `justificativas-tecnicas.md` |
| Reutilização de sessão após o usuário encerrar o acesso (sequestro de sessão) | Invalidação da sessão no servidor ao realizar logout | ✅ Implementado | `fluxo-autenticacao.md` |
| Interceptação de dados durante a transmissão (ataque man-in-the-middle) | Comunicação via HTTPS/TLS 1.3, com troca de chaves X25519MLKEM768 (resistente a computação quântica) e cifragem simétrica AES-128-GCM; certificado emitido e renovado automaticamente pelo Render/Cloudflare | ✅ Implementado | `criptografia.md` |
| Ataque de downgrade de protocolo (forçar conexão HTTP não criptografada) | Cabeçalho `Strict-Transport-Security` (HSTS) com `max-age` elevado, `includeSubDomains` e `preload`, obrigando o navegador a usar exclusivamente HTTPS | ✅ Implementado | `criptografia.md` |
| Roubo de cookie de sessão via script malicioso (Cross-Site Scripting — XSS) | Cookies de sessão configurados com atributos `HttpOnly` (bloqueia acesso via JavaScript) e `Secure` (só trafega em conexão criptografada) | ✅ Implementado | `criptografia.md` |
| Incorporação da aplicação em iframe de terceiros (Clickjacking) | Cabeçalho `X-Frame-Options: DENY` | ✅ Implementado | `criptografia.md` |
| Interpretação incorreta de tipo de arquivo pelo navegador (MIME-sniffing) | Cabeçalho `X-Content-Type-Options: nosniff` | ✅ Implementado | `criptografia.md` |
| Exposição de dados sensíveis armazenados em caso de vazamento do banco de dados | Campo customizado `TelefoneCriptografadoField` (`usuarios/models.py`), que criptografa/descriptografa o telefone automaticamente com Fernet (AES-128-CBC + HMAC-SHA256) da biblioteca `cryptography`, usando uma chave (`FIELD_ENCRYPTION_KEY`) separada da `SECRET_KEY` e armazenada apenas em variável de ambiente | ✅ Implementado | `criptografia.md` |

## 2. Riscos identificados, sem contramedida implementada (pendentes)

| Risco / Ameaça | Contramedida planejada | Status | Observação |
|---|---|---|---|
| Tratamento de dados pessoais sem consentimento explícito do titular | Tela de aceite de Termos de Uso e Política de Privacidade (RF10) | ❌ Não implementado | Requisito já definido (RF10), aguardando desenvolvimento |
| Tratamento de dados de estudantes menores de idade sem autorização do responsável | Consentimento obrigatório do responsável legal antes do cadastro (RF50) | ❌ Não implementado | Requisito já definido na v3 (RF50), aguardando desenvolvimento |
| Usuário sem controle sobre os próprios dados (violação dos direitos do titular, LGPD) | Funcionalidades de consulta, exportação e exclusão de dados pessoais (RF11, RF12) | ❌ Não implementado | Requisitos já definidos, aguardando desenvolvimento |
| Retenção indevida de dados por tempo indeterminado | Política de retenção e descarte de dados definida (RNF09) | ❌ Não implementado | Requisito definido, sem implementação técnica ainda |

## 3. Observações

Este documento reflete o estado real do projeto até o momento. A Seção 3 (Criptografia) do checklist técnico está integralmente implementada, tanto em trânsito (TLS/HSTS/cookies seguros) quanto em repouso (campo de telefone criptografado com Fernet). A Seção 4 (Conformidade com a LGPD) ainda está pendente, mas o desenvolvimento do módulo de conformidade LGPD ainda está em andamento.

A camada de segurança em trânsito (TLS 1.3, HSTS, cookies seguros e cabeçalhos de proteção HTTP) foi validada por meio de testes práticos na aplicação em produção (Render), utilizando as ferramentas de Segurança e Rede do navegador (DevTools), confirmando a aplicação correta de todas as configurações descritas na Seção 1.

A criptografia de dados sensíveis em repouso foi confirmada por inspeção direta do código-fonte (`usuarios/models.py`), após atualização do repositório local via `git pull`.

Este documento deve ser atualizado conforme cada contramedida pendente for implementada, movendo o item correspondente da Seção 2 para a Seção 1.

---

> Última atualização: _(20/09/2026)_
> Responsável pela documentação: _(Jhonathan Tonello)_
