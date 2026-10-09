from django.contrib.auth.decorators import login_required
from django.shortcuts import render


@login_required
def gamificacao(request):
    return render(request, 'gamificacao/gamificacao.html')