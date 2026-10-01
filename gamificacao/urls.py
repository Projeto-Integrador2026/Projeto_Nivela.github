from django.urls import path
from . import views

urlpatterns = [
    path('gamificacao/', views.gamificacao, name='gamificacao'),
]