# Criptografia e Comunicação Segura — Projeto Nivela

---

## Estratégia de criptografia (3.7)

### Comunicação segura (TLS/HTTPS)
A comunicação entre cliente e servidor é protegida por **HTTPS/TLS**, fornecido automaticamente pela plataforma de hospedagem **Render**. O Render emite e renova certificados SSL/TLS gratuitamente para aplicações hospedadas em seu free tier, dispensando a necessidade de configuração manual de certificados (RNF05, RNF29).

### Dados sensíveis em repouso (criptografia no banco)
O modelo `Usuario` recebeu um novo campo, `telefone`, implementado através de um campo customizado do Django (`TelefoneCriptografadoField`, em `usuarios/models.py`) que criptografa o valor automaticamente antes de gravar no banco e o descriptografa ao ser lido pela aplicação. A criptografia usa **Fernet**, da biblioteca `cryptography` do Python, que implementa **AES-128 em modo CBC combinado com autenticação HMAC-SHA256**, garantindo tanto confidencialidade quanto integridade dos dados (qualquer alteração no valor criptografado invalida a descriptografia). Testado manualmente em ambiente local via `shell` do Django, confirmando que o valor salvo no banco (consultado via SQL puro) aparece como texto cifrado, enquanto a leitura pelo ORM do Django retorna o valor original corretamente.

### Gerenciamento de chaves
A chave de criptografia (`FIELD_ENCRYPTION_KEY`) é gerada com `Fernet.generate_key()` e mantida **separada da `SECRET_KEY`** do Django, seguindo o princípio de segregação de segredos. Em desenvolvimento, fica no arquivo `.env` local (fora do controle de versão, no `.gitignore`). Em produção, fica configurada como variável de ambiente diretamente no painel do Render, nunca exposta no código-fonte ou no repositório GitHub. As chaves de desenvolvimento e produção são diferentes entre si.

## Justificativa técnica das escolhas (3.8)

A escolha do protocolo de criptografia adotado no sistema baseia-se em três critérios de avaliação: segurança, compatibilidade com o ecossistema tecnológico do projeto e custo de implementação, conforme especificado no requisito não funcional RNF29.

### Segurança (resistência a ataques conhecidos)

Adotou-se o protocolo TLS (Transport Layer Security) na versão 1.3 como mecanismo de criptografia para o tráfego entre cliente e servidor. Segundo a literatura da área, o TLS 1.3 representa uma evolução significativa em relação às versões anteriores do protocolo, uma vez que elimina o suporte a algoritmos criptográficos considerados obsoletos e vulneráveis, reduzindo a superfície de ataque contra técnicas como downgrade attack e interceptação do tipo man-in-the-middle.

No sistema desenvolvido, a troca de chaves criptográficas é realizada por meio do algoritmo X25519MLKEM768, que incorpora resistência a ataques de computação quântica, enquanto a cifragem simétrica dos dados é realizada com AES-128 em modo GCM (Galois/Counter Mode), que garante simultaneamente confidencialidade e autenticidade dos dados transmitidos.

Complementarmente, foram implementados mecanismos adicionais de proteção a nível de cabeçalho HTTP:

- O cabeçalho Strict-Transport-Security (HSTS) obriga o navegador a estabelecer conexões exclusivamente via HTTPS, prevenindo ataques de downgrade de protocolo;
- Os cookies de sessão são configurados com os atributos HttpOnly e Secure, restringindo o acesso via scripts do lado do cliente (mitigação de ataques Cross-Site Scripting — XSS) e impedindo sua transmissão em conexões não criptografadas;
- O cabeçalho X-Content-Type-Options: nosniff previne ataques de interpretação incorreta de tipo MIME;
- O cabeçalho X-Frame-Options: DENY mitiga ataques de clickjacking, impedindo que a aplicação seja incorporada em frames de terceiros.

### Compatibilidade com o ecossistema Django/Python

As configurações de segurança mencionadas são nativas do framework Django, disponibilizadas por meio das diretivas SECURE_HSTS_SECONDS, SESSION_COOKIE_SECURE, SESSION_COOKIE_HTTPONLY, SECURE_CONTENT_TYPE_NOSNIFF e X_FRAME_OPTIONS, dispensando a necessidade de bibliotecas externas para sua implementação. Tal característica está alinhada ao padrão arquitetural MVT (Model-View-Template) adotado pelo projeto e é integralmente suportada pelo servidor de aplicação Gunicorn, responsável pela camada WSGI utilizada no ambiente de produção.

### Custo (RNF29 — ferramentas gratuitas e de código aberto)

A infraestrutura de certificação digital é provida de forma automática pela plataforma de hospedagem (Render), com renovação automática de certificados TLS sem custo adicional. Da mesma forma, todas as configurações de segurança empregadas constituem funcionalidades nativas e gratuitas do framework Django, não havendo dependência de serviços de terceiros pagos para sua implementação, o que atende integralmente ao requisito de utilização de ferramentas gratuitas e de código aberto.

## Decisões técnicas confirmadas

| Pergunta | Decisão |
|---|---|
| O sistema vai usar HTTPS? Onde será hospedado? | Sim, via **Render** (certificado TLS emitido e renovado automaticamente) |
| Quais dados específicos são criptografados em repouso? | Campo **telefone** do `Usuario` (além da senha, que já usa hash) |
| Qual algoritmo/biblioteca é usado para criptografia simétrica? | **Fernet** (AES-128-CBC + HMAC-SHA256), biblioteca `cryptography` |
| Como as chaves de criptografia são geradas e protegidas? | Geradas com `Fernet.generate_key()`, armazenadas em variável de ambiente **separada da `SECRET_KEY`** |

> ✅ Todos os itens do Requisito 3 (Criptografia e Comunicação Segura) foram implementados. A comunicação segura (3.1 a 3.3) foi verificada no site publicado no Render; a criptografia em repouso (3.4 a 3.6) foi testada em ambiente local, e a chave está configurada nas variáveis de ambiente do Render.

## Evidências

Os prints e arquivos que comprovam o funcionamento (itens 3.1 a 3.6) estão em `docs/Evidencias/criptografia-comunicacao-segura/`. O [README dessa pasta](../Evidencias/criptografia-comunicacao-segura/README.md) liga cada arquivo ao item do checklist.

---

> Última atualização: _(20/09/2026)_
> Responsável pela documentação: _(Jhonathan Tonello e Beatriz Miguel)_