# Associação Risco × Contramedida — Projeto Nivela

> Documento de análise de segurança, associando cada risco/ameaça identificado à contramedida correspondente no sistema. Elaborado com base nos documentos já produzidos (`justificativas-tecnicas.md`, `fluxo-autenticacao.md`, `criptografia.md`) e nos Requisitos v3.

## 1. Riscos x contramedida 

| Risco / Ameaça | Contramedida | Status | Documentado em |
|---|---|---|---|
| Exposição de dados sensíveis armazenados em caso de vazamento do banco de dados | Campo telefone criptografado com Fernet (AES-128-CBC + HMAC-SHA256) | ✅ Implementado | `criptografia.md` |
| Ataque de força bruta no login (tentativas repetidas de adivinhar senha) | django-axes: bloqueio da conta após 5 tentativas falhas, cooloff de 1 hora | ✅ Implementado | `justificativas-tecnicas.md` |
| Vazamento de senha em texto plano (banco comprometido) | Hash PBKDF2 com salt único por usuário, nunca armazenando senha em texto plano | ✅ Implementado | `justificativas-tecnicas.md` |
| Acesso indevido usando apenas e-mail/senha vazados | 2FA obrigatório para todos os perfis, via middleware | ✅ Implementado | `justificativas-tecnicas.md` |
| Reutilização de sessão após o usuário encerrar o acesso (sequestro de sessão) | Invalidação da sessão no servidor ao realizar logout | ✅ Implementado | `fluxo-autenticacao.md` |
| Interceptação de dados durante a transmissão (ataque man-in-the-middle) | Comunicação via HTTPS/TLS, com certificado automático fornecido pelo Render | ✅ Implementado | `criptografia.md` |

## 2. Riscos identificados, sem contramedida implementada (pendentes)

| Risco / Ameaça | Contramedida planejada | Status | Observação |
|---|---|---|---|
| Tratamento de dados pessoais sem consentimento explícito do titular | Tela de aceite de Termos de Uso e Política de Privacidade (RF10) | ❌ Não implementado | Requisito já definido (RF10), aguardando desenvolvimento |
| Tratamento de dados de estudantes menores de idade sem autorização do responsável | Consentimento obrigatório do responsável legal antes do cadastro (RF50) | ❌ Não implementado | Requisito já definido na v3 (RF50), aguardando desenvolvimento |
| Usuário sem controle sobre os próprios dados (violação dos direitos do titular, LGPD) | Funcionalidades de consulta, exportação e exclusão de dados pessoais (RF11, RF12) | ❌ Não implementado | Requisitos já definidos, aguardando desenvolvimento |
| Retenção indevida de dados por tempo indeterminado | Política de retenção e descarte de dados definida (RNF09) | ❌ Não implementado | Requisito definido, sem implementação técnica ainda |

## 3. Observações

Este documento reflete o estado real do projeto até o momento. As seções 3 (Criptografia) já estão implementadas e testadas, 4 (Conformidade com a LGPD) do checklist técnico está parcialmente em implantação, o desenvolvimento dos dados em repouso e do módulo de conformidade LGPD ainda está em andamento.

Este documento deve ser atualizado conforme cada contramedida pendente for implementada, movendo o item correspondente da Seção 2 para a Seção 1.

---

> Última atualização: _(14/09/2026)_
> Responsável pela documentação: _(Jhonathan Tonello)_
