from django.contrib.auth.decorators import login_required
from django.shortcuts import render


@login_required
def turmas(request):
    return render(request, 'turmas/turmas.html')