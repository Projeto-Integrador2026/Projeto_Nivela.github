# syntax=docker/dockerfile:1
# Imagem usada pelo pipeline DevSecOps (DAST) e reaproveitavel no scan de imagem (Trivy).
# Dica de supply chain: depois de estabilizar, fixe a imagem base por digest (@sha256:...).
FROM python:3.11.10-slim-bookworm

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1

# Usuario sem privilegios: a aplicacao nao roda como root
RUN groupadd --system app && useradd --system --gid app --create-home app

WORKDIR /app
RUN chown app:app /app

# Dependencias primeiro (melhor uso de cache de camadas)
COPY requirements.txt .
RUN pip install -r requirements.txt

USER app
COPY --chown=app:app . .

# collectstatic precisa do settings carregado; valores abaixo existem SOMENTE no build
# e nao ficam gravados em runtime (em runtime vem tudo por variaveis de ambiente).
RUN SECRET_KEY=build-only FIELD_ENCRYPTION_KEY=build-only DB_PASSWORD=build-only \
    DATABASE_URL=sqlite:////tmp/build.db \
    python manage.py collectstatic --noinput

EXPOSE 8000

CMD ["sh", "-c", "python manage.py migrate --noinput && exec gunicorn nivela.wsgi:application --bind 0.0.0.0:8000 --workers 2 --access-logfile -"]
