from django.contrib import admin
from django.urls import path, include
from two_factor.urls import urlpatterns as tf_urls
from . import views

urlpatterns = [
    path('', include(tf_urls)),
    path('admin/', admin.site.urls),
    path('', include('lgpd.urls')),
    path('', include('usuarios.urls')),
    path('', include('turmas.urls')),
    path('', include('chat.urls')),
    path('', include('gamificacao.urls')),
    path('', include('nivelamento.urls')),
    path('', views.home, name='home'),
]