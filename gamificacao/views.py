from django.shortcuts import render


def gamificacao(request):
    return render(request, 'gamificacao/gamificacao.html')