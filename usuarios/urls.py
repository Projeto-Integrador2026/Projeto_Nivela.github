from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    # Recuperacao de senha (item 2.1)
    path('recuperar-senha/',
         views.RecuperarSenhaView.as_view(template_name='usuarios/password_reset_form.html'),
         name='password_reset'),
    path('recuperar-senha/enviado/',
         auth_views.PasswordResetDoneView.as_view(template_name='usuarios/password_reset_done.html'),
         name='password_reset_done'),
    path('recuperar-senha/confirmar/<uidb64>/<token>/',
         views.RedefinirSenhaView.as_view(template_name='usuarios/password_reset_confirm.html'),
         name='password_reset_confirm'),
    path('recuperar-senha/concluido/',
         auth_views.PasswordResetCompleteView.as_view(template_name='usuarios/password_reset_complete.html'),
         name='password_reset_complete'),

    # Cadastro de novos usuarios
    path('cadastro/', views.CadastroView.as_view(), name='cadastro'),

    # Logout (o Django 5 so aceita sair via POST, feito pelo botao Sair do menu)
    path('sair/', auth_views.LogoutView.as_view(), name='logout'),
]