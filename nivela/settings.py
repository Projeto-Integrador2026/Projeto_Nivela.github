"""
Configurações do Django para o Projeto Nivela.

Este arquivo reúne as definições de ambiente, segurança, banco de dados,
autenticação (2FA, Axes), internacionalização, arquivos estáticos e logging
de auditoria em conformidade com as diretrizes da OWASP e da LGPD.
"""

import os
from pathlib import Path
from urllib.parse import quote
import dj_database_url
from decouple import config

# ==============================================================================
# 1. DIRETÓRIOS E AMBIENTE (PATHS & ENVIRONMENT)
# ==============================================================================

# Caminho base do projeto (diretório raiz)
BASE_DIR = Path(__file__).resolve().parent.parent

# Chave secreta da aplicação (lida via variável de ambiente por segurança)
SECRET_KEY = config('SECRET_KEY')

# Chave simétrica Fernet para criptografia de dados sensíveis em repouso (LGPD / Requisito 3.6)
FIELD_ENCRYPTION_KEY = config('FIELD_ENCRYPTION_KEY')

# Modo de depuração: True em desenvolvimento, False em produção (exigência de segurança)
DEBUG = config('DEBUG', default=False, cast=bool)

# Domínios e IPs autorizados a servir a aplicação (Proteção contra Host Header Injection)
ALLOWED_HOSTS = config(
    'ALLOWED_HOSTS',
    default='127.0.0.1,localhost',
    cast=lambda v: [s.strip() for s in v.split(',')]
)


# ==============================================================================
# 2. DEFINIÇÃO DA APLICAÇÃO (INSTALLED APPS & MIDDLEWARE)
# ==============================================================================

INSTALLED_APPS = [
    # Apps nativos do Django
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # Pacotes de terceiros (Autenticação e Segurança)
    'django_otp',
    'django_otp.plugins.otp_totp',
    'django_otp.plugins.otp_static',
    'two_factor',
    'axes',

    # Módulos customizados do Projeto Nivela
    'usuarios',
    'turmas',
    'gamificacao',
    'lgpd',
    'chat',
    'nivelamento',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    # Servimento eficiente de arquivos estáticos em produção (sem necessidade de Nginx)
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    # Middleware de Autenticação em Dois Fatores (2FA)
    'django_otp.middleware.OTPMiddleware',
    # Middlewares customizados do projeto
    'usuarios.middleware.LoginRequiredMiddleware',
    'usuarios.middleware.Force2FASetupMiddleware',
    # Middleware de proteção contra força bruta
    'axes.middleware.AxesMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'nivela.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'nivela.wsgi.application'


# ==============================================================================
# 3. BANCO DE DADOS (DATABASE CONFIGURATION)
# ==============================================================================

# Em produção (Render), dj_database_url lê automaticamente a variável DATABASE_URL.
# Em desenvolvimento local, conecta ao PostgreSQL na porta 5433.
DATABASES = {
    'default': dj_database_url.config(
        default=f"postgresql://postgres:{quote(config('DB_PASSWORD'), safe='')}@localhost:5433/nivela_db",
        conn_max_age=600,
    )
}

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


# ==============================================================================
# 4. AUTENTICAÇÃO, SENHAS E SESSÕES (AUTH & SECURITY POLICIES)
# ==============================================================================

# Modelo customizado de usuário (suporte a login por e-mail, RF02)
AUTH_USER_MODEL = 'usuarios.Usuario'

# Algoritmo e parâmetro de custo para hash de senhas (PBKDF2 com 1.000.000 de iterações - OWASP 2025+)
AUTH_PASSWORD_HASHERS = [
    'django.contrib.auth.hashers.PBKDF2PasswordHasher',
]

# Validadores de complexidade de senha
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

# Backends de autenticação (Suporte ao Axes + ModelBackend nativo)
AUTHENTICATION_BACKENDS = [
    'axes.backends.AxesStandaloneBackend',
    'django.contrib.auth.backends.ModelBackend',
]

# Gerenciamento de Sessão (Expiração após 30 min de inatividade - Requisitos 1.9 e 1.10)
SESSION_COOKIE_AGE = 1800  # 30 minutos em segundos
SESSION_SAVE_EVERY_REQUEST = True  # Renova o tempo a cada requisição ativa
SESSION_EXPIRE_AT_BROWSER_CLOSE = True  # Encerra a sessão ao fechar o navegador


# ==============================================================================
# 5. AUTENTICAÇÃO EM DOIS FATORES E REDIRECIONAMENTOS (2FA CONFIGURATION)
# ==============================================================================

LOGIN_URL = 'two_factor:login'
LOGIN_REDIRECT_URL = 'two_factor:profile'
LOGOUT_REDIRECT_URL = 'two_factor:login'

# Exige obrigatoriamente 2FA para acesso ao painel administrativo /admin/ (A-01)
TWO_FACTOR_PATCH_ADMIN = True


# ==============================================================================
# 6. PROTEÇÃO CONTRA FORÇA BRUTA (DJANGO-AXES & PROXY DE REDE)
# ==============================================================================

# Limite de tentativas de login inválidas antes do bloqueio temporário (Item 1.11)
AXES_FAILURE_LIMIT = 5  # Bloqueia após 5 tentativas incorretas
AXES_COOLOFF_TIME = 1   # Duração do bloqueio: 1 hora
AXES_LOCKOUT_PARAMETERS = ['username', 'ip_address']

# Mapeamento do campo de e-mail enviado pelo formulário 2FA (auth-username)
AXES_USERNAME_CALLABLE = 'usuarios.axes_utils.obter_username_login'

# Ocultação de dados sensíveis na tabela de tentativas (Minimização LGPD)
AXES_SENSITIVE_PARAMETERS = ['username', 'ip_address', 'auth-username', 'auth-password']

# Leitura do IP real do cliente repassado pelo proxy do Cloudflare/Render (A-05)
AXES_IPWARE_META_PRECEDENCE_ORDER = [
    'HTTP_CF_CONNECTING_IP',
    'HTTP_X_FORWARDED_FOR',
    'REMOTE_ADDR',
]


# ==============================================================================
# 7. COMUNICAÇÃO E SEGURANÇA HTTP/HTTPS (SECURITY HEADERS)
# ==============================================================================

# Configurações ativas apenas quando DEBUG=False (Produção)
SECURE_SSL_REDIRECT = not DEBUG
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
SESSION_COOKIE_SECURE = not DEBUG
CSRF_COOKIE_SECURE = not DEBUG

# HTTP Strict Transport Security (HSTS)
SECURE_HSTS_SECONDS = 31536000 if not DEBUG else 0  # 1 ano
SECURE_HSTS_INCLUDE_SUBDOMAINS = not DEBUG
SECURE_HSTS_PRELOAD = not DEBUG


# ==============================================================================
# 8. SERVIÇO DE E-MAIL E RECUPERAÇÃO DE SENHA (EMAIL & PASSWORD RESET)
# ==============================================================================

# Em desenvolvimento (DEBUG=True), imprime e-mails no console.
# Em produção (DEBUG=False), envia por SMTP (Gmail) via variáveis de ambiente (A-02).
if DEBUG:
    EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
else:
    EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
    EMAIL_HOST = config('EMAIL_HOST', default='smtp.gmail.com')
    EMAIL_PORT = config('EMAIL_PORT', default=587, cast=int)
    EMAIL_USE_TLS = config('EMAIL_USE_TLS', default=True, cast=bool)
    EMAIL_HOST_USER = config('EMAIL_HOST_USER', default='')
    EMAIL_HOST_PASSWORD = config('EMAIL_HOST_PASSWORD', default='')

DEFAULT_FROM_EMAIL = config('DEFAULT_FROM_EMAIL', default='Nivela <nao-responder@localhost>')

# Expiração do token de redefinição de senha (1 hora por segurança, reduzido dos 3 dias padrão)
PASSWORD_RESET_TIMEOUT = 3600


# ==============================================================================
# 9. ARQUIVOS ESTÁTICOS E INTERNACIONALIZAÇÃO (STATIC & I18N)
# ==============================================================================

LANGUAGE_CODE = 'pt-br'
TIME_ZONE = 'America/Sao_Paulo'
USE_I18N = True
USE_TZ = True

STATIC_URL = 'static/'
STATICFILES_DIRS = [BASE_DIR / 'static']
STATIC_ROOT = BASE_DIR / 'staticfiles'

STORAGES = {
    "staticfiles": {
        "BACKEND": "whitenoise.storage.CompressedManifestStaticFilesStorage",
    },
}


# ==============================================================================
# 10. LOGGING E AUDITORIA (LOGGING CONFIGURATION & FILE PERMISSIONS)
# ==============================================================================

# Criação do diretório de logs caso não exista
(BASE_DIR / 'logs').mkdir(exist_ok=True)

# Restrição de permissões de leitura/escrita no ambiente Linux/POSIX (POSIX 0700)
if os.name == 'posix':
    os.chmod(BASE_DIR / 'logs', 0o700)

# Estrutura de logs de auditoria criptográfica e encadeada (Itens 2.6, 2.7, 5.1 e 5.3)
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'com_data': {
            'format': '{asctime} {levelname} {message}',
            'style': '{',
            'datefmt': '%Y-%m-%d %H:%M:%S',
        },
    },
    'handlers': {
        'file_recuperacao_senha': {
            'level': 'INFO',
            'class': 'nivela.logging_utils.FileHandlerComHashEncadeado',
            'filename': BASE_DIR / 'logs' / 'recuperacao_senha.log',
            'formatter': 'com_data',
            'encoding': 'utf-8',
        },
        'file_autenticacao': {
            'level': 'INFO',
            'class': 'nivela.logging_utils.FileHandlerComHashEncadeado',
            'filename': BASE_DIR / 'logs' / 'autenticacao.log',
            'formatter': 'com_data',
            'encoding': 'utf-8',
        },
    },
    'loggers': {
        'usuarios.recuperacao_senha': {
            'handlers': ['file_recuperacao_senha'],
            'level': 'INFO',
            'propagate': True,
        },
        'usuarios.autenticacao': {
            'handlers': ['file_autenticacao'],
            'level': 'INFO',
            'propagate': True,
        },
    },
}