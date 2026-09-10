# Criptografia e Comunicação Segura — Projeto Nivela

> Status: em desenvolvimento. Documento a ser confirmado/completado após a implementação.

## Estratégia de criptografia (3.7)

### Comunicação segura (TLS/HTTPS)
A comunicação entre cliente e servidor é protegida por **HTTPS/TLS**, fornecido automaticamente pela plataforma de hospedagem **Render**. O Render emite e renova certificados SSL/TLS gratuitamente para aplicações hospedadas em seu free tier, dispensando a necessidade de configuração manual de certificados (RNF05, RNF29).

### Dados sensíveis em repouso (criptografia no banco)
_(a definir)_ — descrever quais dados serão criptografados (ex: dados pessoais sensíveis, se houver algum além da senha) e qual algoritmo será usado (ex: AES-256 via biblioteca `cryptography` do Python, ou `django-cryptography`).

### Gerenciamento de chaves
_(a definir)_ — descrever onde as chaves de criptografia ficam armazenadas (ex: variável de ambiente no `.env`, nunca no código-fonte).

## Justificativa técnica das escolhas (3.8)

_(a definir após a implementação)_ — explicar por que o algoritmo escolhido é adequado, considerando:
- Segurança (resistência a ataques conhecidos)
- Compatibilidade com o ecossistema Django/Python
- Custo (RNF29: ferramentas gratuitas/open-source)

## Pendências a confirmar após a implementação

- [x] O sistema vai usar HTTPS? Onde será hospedado? → **Sim, via Render (certificado automático)**
- [ ] Quais dados específicos serão criptografados em repouso (além da senha, que já usa hash)?
- [ ] Qual algoritmo/biblioteca será usado para criptografia simétrica (ex: AES)?
- [ ] Como as chaves de criptografia serão geradas e protegidas?

## Evidências

> Prints e capturas comprovando o funcionamento real (item 3.3 e ACE02/ACE03 do checklist). Adicionar assim que a funcionalidade estiver implementada e testada.



---

> Última atualização: _(10/09/2026)_
> Responsável pela documentação: _(Jhonathan Tonello)_
