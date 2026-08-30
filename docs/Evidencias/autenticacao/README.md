\# Evidências - Autenticação



\## Teste de login no admin do Django



Testamos o acesso ao painel administrativo (/admin/) usando um superusuário

criado localmente com o comando createsuperuser.



Como foi feito o teste:

1\. Subimos o servidor local com o comando runserver.

2\. Acessamos http://127.0.0.1:8000/admin/login/ pelo navegador.

3\. Fizemos login com o usuário e senha criados.



Resultado: o login funcionou normalmente. Depois de entrar, o painel

mostrou as opções padrão do Django (Users, Groups) e também as do

django-axes (Access attempts, Access failures, Access logs), que é a

proteção contra tentativas de força bruta que o projeto usa. Isso mostra

que o login e essa proteção estão funcionando juntos.



Stack usada no teste: Django 6.1 + PostgreSQL (porta 5433) + django-axes.



\## Prints



!\[Tela de login vazia](print-login.png)

Tela de login antes de entrar com o usuário.



!\[Login feito com sucesso](print-login-sucesso.png)

Painel depois do login, mostrando os módulos de autenticação e do axes.

