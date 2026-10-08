from django.shortcuts import render


def nivelamento(request):
    return render(request, 'nivelamento/nivelamento.html')