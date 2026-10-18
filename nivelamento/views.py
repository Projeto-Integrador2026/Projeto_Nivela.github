from django.contrib.auth.decorators import login_required
from django.shortcuts import render


@login_required
def nivelamento(request):
    return render(request, 'nivelamento/nivelamento.html')