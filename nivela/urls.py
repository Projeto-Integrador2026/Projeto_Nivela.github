from usuarios import views as usuarios_views
from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views
from . import views
from two_factor.urls import urlpatterns as tf_urls

urlpatterns = [
    path('', include(tf_urls)),
    path('admin/', admin.site.urls),

    # Recuperacao de senha (item 2.1) - views prontas do Django
    path('recuperar-senha/',
         usuarios_views.RecuperarSenhaView.as_view(template_name='usuarios/password_reset_form.html'),
         name='password_reset'),
    path('recuperar-senha/enviado/',
         auth_views.PasswordResetDoneView.as_view(template_name='usuarios/password_reset_done.html'),
         name='password_reset_done'),
    path('recuperar-senha/confirmar/<uidb64>/<token>/',
         usuarios_views.RedefinirSenhaView.as_view(template_name='usuarios/password_reset_confirm.html'),
         name='password_reset_confirm'),
    path('recuperar-senha/concluido/',
         auth_views.PasswordResetCompleteView.as_view(template_name='usuarios/password_reset_complete.html'),
         name='password_reset_complete'),

    path('', views.home, name='home'),
    path('turmas/', views.turmas, name='turmas'),
    path('chat/', views.chat, name='chat'),
    path('gamificacao/', views.gamificacao, name='gamificacao'),
]