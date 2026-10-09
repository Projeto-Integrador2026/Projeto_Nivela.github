from django.urls import path
from . import views

app_name = 'nivelamento'

urlpatterns = [
    path('nivelamento/', views.nivelamento, name='nivelamento'),
]