from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_POST

from .models import RegistroConsentimento


@login_required
def meus_consentimentos(request):
    """
    Tela "Meus consentimentos": lista os consentimentos do titular logado
    e permite revogar os que estao ativos (item 4.6 do checklist LGPD).
    """
    consentimentos = RegistroConsentimento.objects.filter(usuario=request.user)
    return render(request, 'lgpd/meus_consentimentos.html', {
        'consentimentos': consentimentos,
    })


@login_required
@require_POST
def revogar_consentimento(request, pk):
    """
    Revoga um consentimento especifico do titular logado (item 4.6).
    Mantem o historico (nao apaga o registro): so marca como revogado
    e grava a data da revogacao, usando o metodo revogar() do model.
    """
    consentimento = get_object_or_404(
        RegistroConsentimento, pk=pk, usuario=request.user
    )
    consentimento.revogar()
    messages.success(request, 'Consentimento revogado com sucesso.')
    return redirect('lgpd:meus_consentimentos')