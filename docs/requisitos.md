# Stack Tecnológica
 
O projeto será desenvolvido utilizando **Python** e o framework **Django**, com **PostgreSQL** como sistema gerenciador de banco de dados.
 
A interface será desenvolvida utilizando:
 
- **HTML5**
- **CSS3**
- **JavaScript**
 
O controle de versão será realizado utilizando **Git** e **GitHub**.
 
# Arquitetura
 
A aplicação utilizará a arquitetura **MVT (Model-View-Template)**, padrão do framework Django.
 
A arquitetura será organizada de forma modular, separando:
 
- Autenticação
- Regras de negócio
- Apresentação
- Persistência de dados
 
O Django será responsável pelo processamento das requisições, gerenciamento de usuários, controle de acesso e comunicação com o banco de dados **PostgreSQL**.
 
## Estrutura da Arquitetura
 
```text
Usuário
   │
   ▼
Interface Web
HTML5 + CSS3 + JavaScript
   │
   ▼
Django
   │
   ├── Views
   ├── Templates
   ├── Models
   ├── Autenticação e Autorização
   └── Regras de Negócio
   │
   ▼
PostgreSQL
