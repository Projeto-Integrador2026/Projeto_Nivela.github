# Nivela

Plataforma de nivelamento de ensino gamificada em turmas, desenvolvida como Projeto Integrador do curso de Engenharia de Software (UMC). Combina regras de negócio inspiradas no Duolingo (Trilhas de aprendizados, agrupamento por níveis, gameficação, análise de nível, análise de habilidade e rankig) com as do Microsoft Teams (turmas, avisos, chat interativo).

## Equipe

- **Beatriz** — Back-end, front end e Banco de Dados
- **Jhonathan Tonello** — Documentação
- **Vinicius Rodrigues** — Front-end e Layout
- Professor responsável: Fabiano M.

## Tecnologias

- **Back-end:** Python / Django (arquitetura MVT)
- **Banco de dados:** PostgreSQL
- **Front-end:** HTML5, CSS3, JavaScript
- **Segurança:** `django-two-factor-auth` (2FA), `django-axes` (proteção contra força bruta), hash de senha PBKDF2-SHA256

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
DB_PASSWORD=sua_senha_do_postgresql_aqui
```
> Peça esses valores para um integrante da equipe — nunca são compartilhados no repositório.

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
- [Documentação Técnico-Científica](./docs/Documentacao-Tecnico-Cientifica) (fluxos de autenticação e recuperação de senha, justificativas técnicas)
- [Checklist de requisitos](./docs/checklist.md)
- [Evidências funcionais](./docs/Evidencias)

## Licença

Este projeto está sob a licença Apache-2.0 — veja o arquivo [LICENSE](./LICENSE) para mais detalhes.