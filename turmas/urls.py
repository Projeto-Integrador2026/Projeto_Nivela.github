from django.urls import path
from . import views

urlpatterns = [
    path('turmas/', views.turmas, name='turmas'),
]