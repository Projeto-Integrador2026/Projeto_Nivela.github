from django.contrib.auth.models import AbstractUser
from django.conf import settings
from django.db import models
from cryptography.fernet import Fernet


class TelefoneCriptografadoField(models.CharField):
    """
    Campo customizado que criptografa o telefone antes de salvar no
    banco e descriptografa automaticamente ao ler (item 3.4 e 3.5
    do Requisito 3). Usa Fernet (AES-128-CBC + HMAC-SHA256) da
    biblioteca 'cryptography', com uma chave separada da SECRET_KEY,
    guardada em variavel de ambiente (item 3.6).
    """

    def _fernet(self):
        return Fernet(settings.FIELD_ENCRYPTION_KEY.encode())

    def get_prep_value(self, value):
        # Chamado antes de salvar no banco: criptografa o texto puro
        if value is None or value == '':
            return value
        if isinstance(value, bytes):
            return value.decode()
        valor_criptografado = self._fernet().encrypt(value.encode())
        return valor_criptografado.decode()

    def from_db_value(self, value, expression, connection):
        # Chamado ao ler do banco: descriptografa de volta para texto puro
        if value is None or value == '':
            return value
        return self._fernet().decrypt(value.encode()).decode()


class Usuario(AbstractUser):
    """
    Usuario customizado do Nivela.
    Estende o AbstractUser padrao do Django, mas troca o campo
    de login de 'username' para 'email' (RF02: login por e-mail e senha).
    """
    email = models.EmailField('endereco de email', unique=True)

    # Telefone criptografado em repouso no banco (Requisito 3.4-3.6).
    # max_length maior que um telefone normal porque o texto
    # criptografado (Fernet) ocupa mais espaço que o texto original.
    telefone = TelefoneCriptografadoField(
        'telefone', max_length=255, blank=True, null=True
    )

    # Define que o campo usado para autenticar (login) e o email,
    # em vez do username padrao do Django.
    USERNAME_FIELD = 'email'

    # Campos obrigatorios alem do USERNAME_FIELD ao criar um
    # superusuario via linha de comando (username continua existindo
    # no banco, mas nao e mais usado para login).
    REQUIRED_FIELDS = ['username']

    def __str__(self):
        return self.email