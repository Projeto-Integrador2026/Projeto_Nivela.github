from django.shortcuts import render


def turmas(request):
    return render(request, 'turmas/turmas.html')