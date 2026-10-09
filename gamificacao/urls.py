from django.urls import path
from . import views

app_name = 'gamificacao'

urlpatterns = [
    path('gamificacao/', views.gamificacao, name='gamificacao'),
]