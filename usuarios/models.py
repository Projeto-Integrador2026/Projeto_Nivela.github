from django.contrib.auth.models import AbstractUser
from django.db import models


class Usuario(AbstractUser):
    """
    Usuario customizado do Nivela.
    Estende o AbstractUser padrao do Django, mas troca o campo
    de login de 'username' para 'email' (RF02: login por e-mail e senha).
    """
    email = models.EmailField('endereco de email', unique=True)

    # Define que o campo usado para autenticar (login) e o email,
    # em vez do username padrao do Django.
    USERNAME_FIELD = 'email'

    # Campos obrigatorios alem do USERNAME_FIELD ao criar um
    # superusuario via linha de comando (username continua existindo
    # no banco, mas nao e mais usado para login).
    REQUIRED_FIELDS = ['username']

    def __str__(self):
        return self.email