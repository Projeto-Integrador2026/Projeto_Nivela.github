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
| Tratamento de dados de estudantes menores de idade sem autorização do responsável | Consentimento obrigatório do responsável legal antes do cadastro, via entidades `responsaveis_legais` e `consentimentos_responsavel` (RF50) | ✅ Implementado | `der.md`, evidências em `docs/Evidencias/lgpd/` |
| Tratamento de dados pessoais sem consentimento explícito do titular | Tela de aceite de Termos de Uso e Política de Privacidade (RF10) | ✅ Implementado | evidências em `docs/Evidencias/lgpd/` |
| Usuário sem controle sobre os próprios dados (violação dos direitos do titular, LGPD) | Funcionalidades de consulta, exportação e exclusão de dados pessoais (RF11, RF12) | ✅ Implementado | evidências em `docs/Evidencias/lgpd/` |
| Retenção indevida de dados por tempo indeterminado | Política de retenção e descarte de dados definida (RNF09) | ✅ Implementado | evidências em `docs/Evidencias/lgpd/` |

## 2. Riscos aceitos ou com limitação conhecida

Riscos que o grupo decidiu aceitar, ou que dependem de uma limitação de infraestrutura. As decisões completas estão na Seção 9 do `checklist.md`.

| Risco / Ameaça | Situação | Contramedida parcial | Status | Plano |
|---|---|---|---|---|
| Cadastro com o e-mail de outra pessoa, e criação do primeiro autenticador 2FA por quem cadastrou (e-mail não verificado, achado A-06) | O plano gratuito do Render bloqueia o SMTP; a verificação por e-mail foi removida e a conta nasce ativa | 2FA obrigatório; aceite de termos registrado; hash PBKDF2; bloqueio por tentativas (django-axes) | ⚠️ Risco aceito pelo grupo (DEC-01). Severidade: Média | Reativar a verificação com plano pago ou serviço de e-mail por API HTTP |
| Usuário sem como redefinir a senha por e-mail em produção | O e-mail de redefinição não é entregue pelo mesmo bloqueio de SMTP | Fluxo implementado e testado no código (itens 2.1 a 2.7 do checklist) | ⚠️ Limitação de infraestrutura (DEC-02) | Resolvido junto com a DEC-01 |

## 3. Observações

Este documento reflete o estado real do projeto até o momento. As Seções 3 (Criptografia) e 4 (Conformidade com a LGPD) do checklist técnico estão integralmente implementadas: criptografia em trânsito (TLS/HSTS/cookies seguros) e em repouso (campo de telefone criptografado com Fernet), além do consentimento do responsável legal para menores (RF50), do consentimento explícito do titular (RF10), das funcionalidades de consulta/exportação/exclusão de dados (RF11, RF12) e da política de retenção de dados (RNF09).

A camada de segurança em trânsito (TLS 1.3, HSTS, cookies seguros e cabeçalhos de proteção HTTP) foi validada por meio de testes práticos na aplicação em produção (Render), utilizando as ferramentas de Segurança e Rede do navegador (DevTools), confirmando a aplicação correta de todas as configurações descritas na Seção 1.

A criptografia de dados sensíveis em repouso foi confirmada por inspeção direta do código-fonte (`usuarios/models.py`), após atualização do repositório local via `git pull`.

Os itens da LGPD (RF10, RF11, RF12, RF50, RNF09) foram confirmados por meio de evidências funcionais (`docs/Evidencias/lgpd/`).

O envio de e-mail por SMTP não funciona na hospedagem atual (Render, plano gratuito), conforme o aviso do próprio provedor sobre o bloqueio das portas 25, 465 e 587. Por isso a conta criada no cadastro nasce ativa, sem e-mail de ativação, e a redefinição de senha não entrega o link em produção. A decisão e o risco residual estão na Seção 2 deste documento e na Seção 9 do `checklist.md`.

---

> Última atualização: _(18/10/2026)_
> Responsável pela documentação: _(Jhonathan Tonello e Beatriz Miguel)_
