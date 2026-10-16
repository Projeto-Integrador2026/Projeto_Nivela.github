"""
Módulo de Views da LGPD (Lei Geral de Proteção de Dados - Lei nº 13.709/2018).

Este arquivo reúne as visões responsáveis por garantir os direitos dos titulares de dados
(consulta, confirmação, portabilidade, revogação de consentimento e eliminação de dados)
e a exibição dos documentos legais (Termos de Uso e Política de Privacidade).
"""

import json
import uuid

from django.contrib import messages
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.http import HttpRequest, HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone
from django.views.decorators.http import require_POST
from django.views.generic import TemplateView

# Módulos de terceiros e do projeto para segurança e auditoria
from axes.models import AccessAttempt, AccessFailureLog, AccessLog
from django_otp.plugins.otp_totp.models import TOTPDevice

from gamificacao.models import (
    PerfilGamificacao,
    ProgressoLicao,
    ResultadoNivelamento,
    TentativaExercicio,
)
from .models import RegistroConsentimento, SolicitacaoTitular


# ==============================================================================
# 1. DIREITOS DO TITULAR - CONSULTA E PORTABILIDADE (LGPD ART. 18, II e V)
# ==============================================================================

@login_required
def meus_dados(request: HttpRequest) -> HttpResponse:
    """
    Tela "Meus dados": garante a confirmação da existência de tratamento e o acesso
    aos dados pessoais do titular (LGPD, Art. 18, I e II / Requisito 4.8).

    Registra a solicitação de acesso na tabela SolicitacaoTitular para auditoria (A-13).
    """
    usuario = request.user

    # Registra o atendimento ao direito de acesso (A-13)
    SolicitacaoTitular.objects.create(
        usuario=usuario,
        identificador_anonimo=uuid.uuid4().hex,
        tipo=SolicitacaoTitular.Tipo.ACESSO,
        status=SolicitacaoTitular.Status.CONCLUIDA,
        data_conclusao=timezone.now(),
        detalhes="Consulta realizada pelo titular à tela Meus Dados."
    )

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
def exportar_dados(request: HttpRequest) -> HttpResponse:
    """
    Exportação dos dados pessoais do titular em formato JSON para download.
    Garante a portabilidade dos dados (LGPD, Art. 18, V / Requisito 4.9).

    Registra a solicitação de exportação na tabela SolicitacaoTitular para auditoria (A-13).
    """
    usuario = request.user

    # Registra o atendimento ao direito de portabilidade/exportação (A-13)
    SolicitacaoTitular.objects.create(
        usuario=usuario,
        identificador_anonimo=uuid.uuid4().hex,
        tipo=SolicitacaoTitular.Tipo.EXPORTACAO,
        status=SolicitacaoTitular.Status.CONCLUIDA,
        data_conclusao=timezone.now(),
        detalhes="Exportação de dados em formato JSON efetuada pelo titular."
    )

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


# ==============================================================================
# 2. DIREITOS DO TITULAR - GESTÃO E REVOGAÇÃO DE CONSENTIMENTO (LGPD ART. 8º §5º)
# ==============================================================================

@login_required
def meus_consentimentos(request: HttpRequest) -> HttpResponse:
    """
    Tela "Meus consentimentos": lista os consentimentos registrados para o titular logado
    e permite a gestão e revogação das finalidades ativas (LGPD, Art. 8º / Requisito 4.6).
    """
    consentimentos = RegistroConsentimento.objects.filter(usuario=request.user)
    return render(request, 'lgpd/meus_consentimentos.html', {
        'consentimentos': consentimentos,
    })


@login_required
@require_POST
@transaction.atomic
def revogar_consentimento(request: HttpRequest, pk: int) -> HttpResponse:
    """
    Revoga um consentimento específico do titular logado (LGPD, Art. 8º §5º).

    Mantém o histórico para fins de comprovação regulatória, marca o registro como revogado
    e grava uma SolicitacaoTitular do tipo REVOGACAO (A-13).
    """
    consentimento = get_object_or_404(
        RegistroConsentimento, pk=pk, usuario=request.user
    )
    consentimento.revogar()

    SolicitacaoTitular.objects.create(
        usuario=request.user,
        identificador_anonimo=uuid.uuid4().hex,
        tipo=SolicitacaoTitular.Tipo.REVOGACAO,
        status=SolicitacaoTitular.Status.CONCLUIDA,
        data_conclusao=timezone.now(),
        detalhes=f"Revogação do consentimento para a finalidade: {consentimento.get_finalidade_display()}"
    )

    messages.success(request, 'Consentimento revogado com sucesso.')
    return redirect('lgpd:meus_consentimentos')


# ==============================================================================
# 3. DIREITOS DO TITULAR - ELIMINAÇÃO DE DADOS / EXCLUSÃO DE CONTA (LGPD ART. 18, VI)
# ==============================================================================

@login_required
@transaction.atomic
def excluir_conta(request: HttpRequest) -> HttpResponse:
    """
    Exclusão definitiva da conta e eliminação dos dados pessoais (LGPD, Art. 18, VI / Requisito 4.10).

    Garante atomicidade da operação (@transaction.atomic), limpa dados de tentativas
    no django-axes (A-12) e registra o protocolo anônimo de atendimento (A-13).
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
            email_usuario = usuario.email
            identificador = uuid.uuid4().hex

            # 1. Registra o protocolo de atendimento da solicitação de exclusão (A-13)
            SolicitacaoTitular.objects.create(
                usuario=usuario,
                identificador_anonimo=identificador,
                tipo=SolicitacaoTitular.Tipo.EXCLUSAO,
                status=SolicitacaoTitular.Status.CONCLUIDA,
                data_conclusao=timezone.now(),
                detalhes="Eliminação definitiva de conta e dados pessoais efetuada pelo titular."
            )

            # 2. Limpa registros associados no django-axes para garantir exclusão completa (A-12)
            AccessAttempt.objects.filter(username__iexact=email_usuario).delete()
            AccessLog.objects.filter(username__iexact=email_usuario).delete()
            AccessFailureLog.objects.filter(username__iexact=email_usuario).delete()

            # 3. Apaga a conta do usuário e desloga
            usuario.delete()
            logout(request)

            messages.success(
                request,
                f'Sua conta e todos os seus dados pessoais foram excluídos com sucesso. '
                f'Protocolo de atendimento: {identificador}'
            )
            return redirect('two_factor:login')

    return render(request, 'lgpd/excluir_conta.html', {'erro': erro})


# ==============================================================================
# 4. DOCUMENTOS LEGAIS E INSTITUCIONAIS (LGPD ART. 8º E ART. 9º)
# ==============================================================================

class TermosUsoView(TemplateView):
    """Exibe a página pública dos Termos de Uso do sistema (A-11 / LGPD, Art. 8º)."""
    template_name = 'lgpd/termos.html'


class PoliticaPrivacidadeView(TemplateView):
    """Exibe a página pública da Política de Privacidade do sistema (A-11 / LGPD, Art. 9º)."""
    template_name = 'lgpd/privacidade.html'