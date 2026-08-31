from django.shortcuts import render


def home(request):
    return render(request, 'home.html')


def turmas(request):
    return render(request, 'turmas.html')


def chat(request):
    return render(request, 'chat.html')


def gamificacao(request):
    return render(request, 'gamificacao.html')
