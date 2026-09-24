release: python manage.py migrate && python manage.py collectstatic --noinput && python manage.py  && python manage.py limpar_dados_expirados
web: gunicorn nivela.wsgi:application