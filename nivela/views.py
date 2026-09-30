from django.shortcuts import render


def home(request):
    return render(request, 'home.html')


def chat(request):
    return render(request, 'chat.html')


def gamificacao(request):
    return render(request, 'gamificacao.html')


def nivelamento(request):
    return render(request, 'nivelamento.html')