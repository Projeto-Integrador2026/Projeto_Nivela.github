# Justificativas Técnicas — Autenticação e Gestão de Credenciais

> Referente à seção 1 do checklist técnico (itens 1.1 a 1.12). Documenta o motivo das escolhas técnicas de segurança, não apenas o que foi implementado.

## 1.1 — Algoritmo de hash de senha

**Escolha:** _(confirmar qual foi usado: Argon2, bcrypt ou PBKDF2)_

**Justificativa (exemplo com bcrypt, ajustar conforme a escolha real):**
> Optou-se pelo uso do **bcrypt** como algoritmo de hash de senha por ser nativamente suportado pelo Django (`django.contrib.auth.hashers`), amplamente testado em produção e utilizado como padrão de mercado. O bcrypt incorpora um *fator de custo* configurável, tornando o cálculo do hash deliberadamente lento — o que dificulta ataques de força bruta e uso de hardware especializado (GPU/ASIC) — atendendo ao RNF10.

> _Se o grupo optou por **Argon2** em vez de bcrypt: Argon2 é considerado o algoritmo mais moderno e resistente (vencedor da Password Hashing Competition), oferecendo proteção adicional contra ataques com GPU/hardware dedicado, por permitir configurar não só tempo de processamento, mas também consumo de memória._

## 1.2 — Parâmetros de custo do hash

**Escolha:** _(preencher com os valores reais usados no código, ex: número de iterações, custo, memória)_

**Justificativa (exemplo genérico — ajustar aos valores reais):**
> Os parâmetros de custo foram configurados em `[valor]`, seguindo a recomendação padrão da biblioteca/framework utilizado para o ano de desenvolvimento do projeto (2026), equilibrando segurança (tempo suficiente para dificultar ataques de força bruta) e desempenho aceitável para o usuário final (RNF17 — resposta em até 2 segundos). Valores mais altos aumentariam a segurança, mas comprometeriam a meta de desempenho definida no projeto.

## 1.3 — Salt criptográfico único por usuário

**Justificativa:**
> Cada senha é protegida por um salt único, gerado automaticamente no momento do cadastro (comportamento padrão do Django ao usar `make_password`). O uso de salt único por usuário impede ataques de *rainbow table* (tabelas pré-computadas de hashes), já que dois usuários com a mesma senha terão hashes finais completamente diferentes, atendendo ao RNF12.

## 1.4 — Armazenamento do hash + salt

**Justificativa:**
> O hash da senha já inclui o salt embutido no próprio valor armazenado (formato padrão do Django: `algoritmo$parâmetros$salt$hash`), evitando a necessidade de uma coluna separada no banco de dados e reduzindo o risco de inconsistência entre hash e salt armazenados separadamente, conforme RNF13.

## 1.9 — Sessões com tempo de expiração

**Escolha:** _(preencher com o tempo real definido, ex: 30 minutos, 2 horas)_

**Justificativa (exemplo):**
> O tempo de expiração da sessão foi definido em `[X minutos/horas]`, equilibrando segurança (reduzir a janela de exposição em caso de sessão esquecida aberta) e usabilidade (evitar que o usuário precise fazer login com frequência excessiva durante o uso normal da plataforma), atendendo ao RNF14.

## 1.10 — Invalidação de sessão no logout

**Justificativa:**
> Ao realizar logout, a sessão do usuário é invalidada no lado do servidor (não apenas removida do navegador do cliente), impedindo que o mesmo token/cookie de sessão seja reutilizado posteriormente, mesmo que capturado por terceiros, atendendo ao RF09.

## 1.5 / 1.6 — Autenticação de dois fatores (2FA) *(ainda não implementado)*

> Conforme RF07 (ajustado na v3 dos requisitos), o 2FA foi classificado como requisito **desejável**, podendo ser postergado para uma versão futura caso o cronograma da disciplina não comporte sua implementação. Caso seja implementado, a validação do segundo fator deve ocorrer apenas após a autenticação primária bem-sucedida (RF08), evitando expor informação sobre a validade do 2FA antes de confirmar e-mail/senha corretos.

## 1.11 — Proteção contra força bruta *(ainda não implementado)*

**Recomendação técnica para quando for implementado:**
> Sugere-se o uso de *rate limiting* (ex: biblioteca `django-ratelimit` ou `django-axes`), bloqueando temporariamente a conta ou aplicando atraso progressivo entre tentativas após um número definido de falhas consecutivas (ex: 5 tentativas), atendendo ao RNF15.

---

> ⚠️ Os campos marcados como "preencher" precisam ser confirmados com quem está desenvolvendo o código, para que a justificativa reflita exatamente o que foi implementado.
>
> Última atualização: _(preencher data)_
> Responsável pela documentação: _(seu nome)_
