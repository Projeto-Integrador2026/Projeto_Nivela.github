from django.contrib import admin
from django.urls import path, include
from . import views
from two_factor.urls import urlpatterns as tf_urls

urlpatterns = [
    path('', include(tf_urls)),
    path('admin/', admin.site.urls),
    path('', views.home, name='home'),
    path('turmas/', views.turmas, name='turmas'),
    path('chat/', views.chat, name='chat'),
    path('gamificacao/', views.gamificacao, name='gamificacao'),
]
