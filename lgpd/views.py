import json
import uuid

from django.contrib import messages
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone
from django.views.decorators.http import require_POST

from django_otp.plugins.otp_totp.models import TOTPDevice

from gamificacao.models import (
    PerfilGamificacao,
    ProgressoLicao,
    ResultadoNivelamento,
    TentativaExercicio,
)

from .models import RegistroConsentimento, SolicitacaoTitular


@login_required
def meus_dados(request):
    """
    Tela "Meus dados": consulta que o titular tem aos proprios dados
    pessoais tratados pelo Nivela (item 4.8 do checklist LGPD).
    """
    usuario = request.user

    tem_2fa = TOTPDevice.objects.filter(user=usuario, confirmed=True).exists()
    perfil = PerfilGamificacao.objects.filter(usuario=usuario).first()
    licoes_concluidas = ProgressoLicao.objects.filter(usuario=usuario, concluida=True).count()
    tentativas_total = TentativaExercicio.objects.filter(usuario=usuario).count()
    tentativas_corretas = TentativaExercicio.objects.filter(usuario=usuario, correta=True).count()
    nivelamento = ResultadoNivelamento.objects.filter(usuario=usuario).order_by('-data').first()

    return render(request, 'lgpd/meus_dados.html', {
        'usuario': usuario,
        'tem_2fa': tem_2fa,
        'perfil': perfil,
        'licoes_concluidas': licoes_concluidas,
        'tentativas_total': tentativas_total,
        'tentativas_corretas': tentativas_corretas,
        'nivelamento': nivelamento,
    })


@login_required
def exportar_dados(request):
    """
    Exportacao dos dados pessoais do titular em formato JSON,
    para download (item 4.9 do checklist LGPD - portabilidade
    de dados, art. 18, V).
    """
    usuario = request.user

    perfil = PerfilGamificacao.objects.filter(usuario=usuario).first()
    progresso = ProgressoLicao.objects.filter(usuario=usuario, concluida=True)
    tentativas = TentativaExercicio.objects.filter(usuario=usuario)
    nivelamento = ResultadoNivelamento.objects.filter(usuario=usuario)
    consentimentos = RegistroConsentimento.objects.filter(usuario=usuario)

    dados = {
        'conta': {
            'email': usuario.email,
            'telefone': usuario.telefone,
            'data_criacao': usuario.date_joined.isoformat(),
            'ultimo_acesso': usuario.last_login.isoformat() if usuario.last_login else None,
        },
        'gamificacao': {
            'xp_total': perfil.xp_total if perfil else 0,
            'nivel': perfil.nivel_calculado if perfil else 1,
            'streak_atual': perfil.streak_atual if perfil else 0,
            'streak_recorde': perfil.streak_recorde if perfil else 0,
            'licoes_concluidas': [
                {
                    'licao_id': p.licao_id,
                    'data_conclusao': p.data_conclusao.isoformat() if p.data_conclusao else None,
                }
                for p in progresso
            ],
            'tentativas_exercicios': [
                {'exercicio_id': t.exercicio_id, 'correta': t.correta, 'data': t.data.isoformat()}
                for t in tentativas
            ],
            'teste_nivelamento': [
                {
                    'trilha_id': n.trilha_id,
                    'modulo_sugerido_id': n.modulo_sugerido_id,
                    'data': n.data.isoformat(),
                }
                for n in nivelamento
            ],
        },
        'consentimentos': [
            {
                'finalidade': c.get_finalidade_display(),
                'versao_termo': c.versao_termo,
                'concedido': c.concedido,
                'data_concessao': c.data_concessao.isoformat() if c.data_concessao else None,
                'data_revogacao': c.data_revogacao.isoformat() if c.data_revogacao else None,
            }
            for c in consentimentos
        ],
    }

    resposta = HttpResponse(
        json.dumps(dados, indent=2, ensure_ascii=False),
        content_type='application/json',
    )
    resposta['Content-Disposition'] = 'attachment; filename="meus-dados-nivela.json"'
    return resposta


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


@login_required
def excluir_conta(request):
    """
    Tela de exclusao da conta e dos dados pessoais do titular
    (item 4.10 do checklist LGPD - direito de eliminacao, art. 18, VI).
    Exige a senha atual como confirmacao antes de excluir de verdade.
    """
    erro = None

    if request.method == 'POST':
        senha = request.POST.get('senha', '')
        confirmou = request.POST.get('confirmar') == 'on'

        if not confirmou:
            erro = 'Marque a caixa de confirmação para excluir sua conta.'
        elif not request.user.check_password(senha):
            erro = 'Senha incorreta.'
        else:
            usuario = request.user
            identificador = uuid.uuid4().hex

            SolicitacaoTitular.objects.create(
                usuario=usuario,
                identificador_anonimo=identificador,
                tipo=SolicitacaoTitular.Tipo.EXCLUSAO,
                status=SolicitacaoTitular.Status.CONCLUIDA,
                data_conclusao=timezone.now(),
            )

            usuario.delete()
            logout(request)
            messages.success(
                request,
                f'Sua conta e todos os seus dados pessoais foram excluídos. '
                f'Protocolo de atendimento: {identificador}'
            )
            return redirect('two_factor:login')

    return render(request, 'lgpd/excluir_conta.html', {'erro': erro})