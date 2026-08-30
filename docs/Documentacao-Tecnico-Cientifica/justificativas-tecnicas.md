# Justificativas Técnicas — Autenticação e Gestão de Credenciais

> Referente à seção 1 do checklist técnico (itens 1.1 a 1.12). Documenta o motivo das escolhas técnicas de segurança, não apenas o que foi implementado.

## 1.1 — Algoritmo de hash de senha

**Justificativa**

> Optou-se pelo uso do PBKDF2 como algoritmo de hash de senha por ser o algoritmo padrão nativo do Django (django.contrib.auth.hashers.PBKDF2PasswordHasher), dispensando a instalação de dependências externas — o que reduz a superfície de manutenção do projeto e está alinhado à restrição de uso de ferramentas gratuitas/open-source do RNF29. O PBKDF2 aplica múltiplas iterações de uma função hash criptográfica (SHA-256, no caso do Django), tornando o cálculo deliberadamente custoso computacionalmente e dificultando ataques de força bruta, atendendo ao RNF10. Por ser recomendado e mantido diretamente pelo próprio framework, também garante que atualizações de segurança futuras (ex: aumento do número padrão de iterações) sejam incorporadas automaticamente em novas versões do Django.

## 1.2 — Parâmetros de custo do hash

**Justificativa**
> Os parâmetros de custo foram configurados em `[1000000]`, seguindo a recomendação padrão da biblioteca/framework utilizado para o ano de desenvolvimento do projeto (2026), equilibrando segurança (tempo suficiente para dificultar ataques de força bruta) e desempenho aceitável para o usuário final (RNF17 — resposta em até 2 segundos). Valores mais altos aumentariam a segurança, mas comprometeriam a meta de desempenho definida no projeto.

## 1.3 — Salt criptográfico único por usuário

**Justificativa:**
> Cada senha é protegida por um salt único, gerado automaticamente no momento do cadastro (comportamento padrão do Django ao usar `make_password`). O uso de salt único por usuário impede ataques de *rainbow table* (tabelas pré-computadas de hashes), já que dois usuários com a mesma senha terão hashes finais completamente diferentes, atendendo ao RNF12.

## 1.4 — Armazenamento do hash + salt

**Justificativa:**
> O hash da senha já inclui o salt embutido no próprio valor armazenado (formato padrão do Django: `algoritmo$parâmetros$salt$hash`), evitando a necessidade de uma coluna separada no banco de dados e reduzindo o risco de inconsistência entre hash e salt armazenados separadamente, conforme RNF13.

## 1.9 — Sessões com tempo de expiração


**Justificativa (exemplo):**
> O tempo de expiração da sessão foi definido em `[30 minutos]`, equilibrando segurança (reduzir a janela de exposição em caso de sessão esquecida aberta) e usabilidade (evitar que o usuário precise fazer login com frequência excessiva durante o uso normal da plataforma), atendendo ao RNF14.

## 1.10 — Invalidação de sessão no logout

**Justificativa:**
> Ao realizar logout, a sessão do usuário é invalidada no lado do servidor (não apenas removida do navegador do cliente), impedindo que o mesmo token/cookie de sessão seja reutilizado posteriormente, mesmo que capturado por terceiros, atendendo ao RF09.

## 1.5 / 1.6 — Autenticação de dois fatores (2FA) 

> Conforme RF07 (ajustado na v3 dos requisitos), o 2FA foi classificado como requisito **desejável**, podendo ser postergado para uma versão futura caso o cronograma da disciplina não comporte sua implementação. Caso seja implementado, a validação do segundo fator deve ocorrer apenas após a autenticação primária bem-sucedida (RF08), evitando expor informação sobre a validade do 2FA antes de confirmar e-mail/senha corretos.

## 1.11 — Proteção contra força bruta 

Status: Implementado, com a biblioteca django-axes

Parâmetros configurados:

Parâmetro	Valor
AXES_FAILURE_LIMIT	5 tentativas
Tempo de bloqueio (cooloff)	1 hora

Justificativa:

Optou-se pela biblioteca django-axes por se integrar nativamente ao sistema de autenticação do Django, sem exigir alterações profundas no fluxo de login já implementado. O limite de 5 tentativas falhas antes do bloqueio segue uma prática comum de mercado, equilibrando segurança (dificultar ataques de força bruta) e usabilidade (tolerância a erros de digitação legítimos do usuário). O período de bloqueio de 1 hora foi definido como tempo suficiente para desestimular ataques automatizados, sem impor um bloqueio excessivamente longo em caso de erro genuíno do usuário, atendendo ao RNF15

> Última atualização: _(30/08/2026)_
> Responsável pela documentação: _(Jhonathan Tonello)_
