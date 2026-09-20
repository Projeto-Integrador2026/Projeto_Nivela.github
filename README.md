# Nivela

Plataforma de nivelamento de ensino gamificada em turmas, desenvolvida como Projeto Integrador do curso de Engenharia de Software (UMC). Combina regras de negócio inspiradas no Duolingo (trilhas de aprendizado, agrupamento por níveis, gamificação, análise de nível, análise de habilidade e ranking) com as do Microsoft Teams (turmas, avisos, chat interativo).

**Site publicado:** https://nivela-cw5t.onrender.com

> O site roda no plano gratuito do Render. Depois de um período sem acesso, a primeira carga pode levar cerca de 50 segundos.

## Equipe

- **Beatriz Miguel** — Back-end, front-end e Banco de Dados
- **Jhonathan Tonello** — Documentação
- **Vinicius Rodrigues** — Front-end e Layout
- Professor responsável: Fabiano M.

## Tecnologias

- **Back-end:** Python / Django (arquitetura MVT)
- **Banco de dados:** PostgreSQL
- **Front-end:** HTML5, CSS3, JavaScript
- **Hospedagem:** Render
- **Segurança:** `django-two-factor-auth` (2FA), `django-axes` (proteção contra força bruta), hash de senha PBKDF2-SHA256, HTTPS/TLS e criptografia de dados sensíveis em repouso com Fernet (`cryptography`)

## Como rodar o projeto localmente

### Pré-requisitos

- Python 3.11+
- PostgreSQL instalado e rodando
- Git

### Passo a passo

1. Clone o repositório:
```bash
   git clone https://github.com/Projeto-Integrador2026/Projeto_Nivela.github.git
   cd Projeto_Nivela.github
```

2. Crie e ative um ambiente virtual:
```bash
   python -m venv venv
   # Windows
   venv\Scripts\activate
   # Linux/Mac
   source venv/bin/activate
```

3. Instale as dependências:
```bash
   pip install -r requirements.txt
```

4. Crie um arquivo `.env` na raiz do projeto com o seguinte conteúdo:
```
   SECRET_KEY=sua_secret_key_aqui
   FIELD_ENCRYPTION_KEY=sua_chave_fernet_aqui
   DB_PASSWORD=sua_senha_do_postgresql_aqui
```
   > A `SECRET_KEY` e a `DB_PASSWORD` devem ser pedidas a um integrante da equipe, pois nunca são compartilhadas no repositório.

   A `FIELD_ENCRYPTION_KEY` (chave de criptografia dos dados sensíveis, que deve ser diferente da `SECRET_KEY`) pode ser gerada localmente:
```bash
   python -c "from cryptography.fernet import Fernet; print(Fernet.generate_key().decode())"
```

5. Crie um banco de dados PostgreSQL chamado `nivela_db`.

6. Rode as migrações:
```bash
   python manage.py migrate
```

7. Inicie o servidor:
```bash
   python manage.py runserver
```

8. Acesse `http://127.0.0.1:8000/` no navegador.

## Documentação

Toda a documentação técnica do projeto está na pasta [`docs/`](./docs), incluindo:

- [Termo de Abertura do Projeto (TAP)](./docs/TAP)
- [Requisitos Funcionais e Não Funcionais](./docs/Requisitos)
- [Casos de Uso](./docs/Casos-de-Uso)
- [Modelo de dados (DER)](./docs/DER)
- [Documentação Técnico-Científica](./docs/Documentacao-Tecnico-Cientifica) (fluxos de autenticação e recuperação de senha, criptografia e comunicação segura, justificativas técnicas, arquitetura e riscos)
- [Checklist de requisitos](./docs/checklist.md)
- [Evidências funcionais](./docs/Evidencias)

## Licença

Este projeto está sob a licença Apache-2.0 — veja o arquivo [LICENSE](./LICENSE) para mais detalhes.