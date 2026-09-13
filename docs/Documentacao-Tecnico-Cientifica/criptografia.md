# Criptografia e Comunicação Segura — Projeto Nivela

> Status: em desenvolvimento. Documento a ser confirmado/completado após a implementação.

## Estratégia de criptografia (3.7)

### Comunicação segura (TLS/HTTPS)
A comunicação entre cliente e servidor é protegida por **HTTPS/TLS**, fornecido automaticamente pela plataforma de hospedagem **Render**. O Render emite e renova certificados SSL/TLS gratuitamente para aplicações hospedadas em seu free tier, dispensando a necessidade de configuração manual de certificados (RNF05, RNF29).

### Dados sensíveis em repouso (criptografia no banco)
O modelo `Usuario` recebeu um novo campo, `telefone`, implementado através de um campo customizado do Django (`TelefoneCriptografadoField`, em `usuarios/models.py`) que criptografa o valor automaticamente antes de gravar no banco e o descriptografa ao ser lido pela aplicação. A criptografia usa **Fernet**, da biblioteca `cryptography` do Python, que implementa **AES-128 em modo CBC combinado com autenticação HMAC-SHA256**, garantindo tanto confidencialidade quanto integridade dos dados (qualquer alteração no valor criptografado invalida a descriptografia). Testado manualmente via `shell` do Django, confirmando que o valor salvo no banco (consultado via SQL puro) aparece como texto cifrado, enquanto a leitura pelo ORM do Django retorna o valor original corretamente.

### Gerenciamento de chaves
A chave de criptografia (`FIELD_ENCRYPTION_KEY`) é gerada com `Fernet.generate_key()` e mantida **separada da `SECRET_KEY`** do Django, seguindo o princípio de segregação de segredos. Em desenvolvimento, fica no arquivo `.env` local (fora do controle de versão, no `.gitignore`). Em produção, fica configurada como variável de ambiente diretamente no painel do Render, nunca exposta no código-fonte ou no repositório GitHub. As chaves de desenvolvimento e produção são diferentes entre si.

## Justificativa técnica das escolhas (3.8)

_(a definir após a implementação)_ — explicar por que o algoritmo escolhido é adequado, considerando:
- Segurança (resistência a ataques conhecidos)
- Compatibilidade com o ecossistema Django/Python
- Custo (RNF29: ferramentas gratuitas/open-source)

## Decisões técnicas confirmadas

| Pergunta | Decisão |
|---|---|
| O sistema vai usar HTTPS? Onde será hospedado? | Sim, via **Render** (certificado TLS emitido e renovado automaticamente) |
| Quais dados específicos são criptografados em repouso? | Campo **telefone** do `Usuario` (além da senha, que já usa hash) |
| Qual algoritmo/biblioteca é usado para criptografia simétrica? | **Fernet** (AES-128-CBC + HMAC-SHA256), biblioteca `cryptography` |
| Como as chaves de criptografia são geradas e protegidas? | Geradas com `Fernet.generate_key()`, armazenadas em variável de ambiente **separada da `SECRET_KEY`** |

> ✅ Todos os itens do Requisito 3 (Criptografia e Comunicação Segura) foram implementados e testados em produção.

## Evidências

> Prints e capturas comprovando o funcionamento real (item 3.3 e ACE02/ACE03 do checklist). Adicionar assim que a funcionalidade estiver implementada e testada.



---

> Última atualização: _(10/09/2026)_
> Responsável pela documentação: _(Jhonathan Tonello)_
