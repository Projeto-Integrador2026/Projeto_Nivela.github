from django.conf import settings
from django.db import models


class Trilha(models.Model):
    nome = models.CharField(max_length=100)  # ex: "Python"
    descricao = models.TextField()
    ativa = models.BooleanField(default=True)


class Tema(models.Model):
    # categoria/assunto do exercício (ex: "Funções", "Laços de repetição"),
    # usado para o painel de desempenho por tema (seção 4.5)
    trilha = models.ForeignKey(Trilha, on_delete=models.CASCADE, related_name='temas')
    nome = models.CharField(max_length=80)


class Modulo(models.Model):
    NIVEL_CHOICES = [
        ('basico', 'Básico'),
        ('intermediario', 'Intermediário'),
        ('avancado', 'Avançado'),
    ]
    trilha = models.ForeignKey(Trilha, on_delete=models.CASCADE, related_name='modulos')
    nome = models.CharField(max_length=100)
    nivel = models.CharField(max_length=20, choices=NIVEL_CHOICES)
    ordem = models.PositiveIntegerField()  # define a sequência (1, 2, 3...)
    percentual_para_liberar = models.PositiveIntegerField(default=80)  # % do módulo anterior necessário

    class Meta:
        ordering = ['trilha', 'ordem']


class Licao(models.Model):
    modulo = models.ForeignKey(Modulo, on_delete=models.CASCADE, related_name='licoes')
    titulo = models.CharField(max_length=150)
    conteudo_teorico = models.TextField()  # texto/markdown explicativo antes dos exercícios
    ordem = models.PositiveIntegerField()

    class Meta:
        ordering = ['modulo', 'ordem']


class Exercicio(models.Model):
    TIPO_CHOICES = [
        ('multipla_escolha', 'Múltipla escolha'),
        ('verdadeiro_falso', 'Verdadeiro ou falso'),
        ('completar_codigo', 'Completar o código'),
        ('ordenar_linhas', 'Ordenar linhas de código'),
    ]
    licao = models.ForeignKey(Licao, on_delete=models.CASCADE, related_name='exercicios')
    tema = models.ForeignKey(Tema, on_delete=models.SET_NULL, null=True, related_name='exercicios')
    tipo = models.CharField(max_length=20, choices=TIPO_CHOICES)
    enunciado = models.TextField()
    resposta_esperada = models.CharField(max_length=255, blank=True)  # só para "completar_codigo"
    xp_recompensa = models.PositiveIntegerField(default=10)
    ordem = models.PositiveIntegerField()
    eh_teste_nivelamento = models.BooleanField(default=False)  # ver seção 4.4


class OpcaoExercicio(models.Model):
    # para multipla_escolha, verdadeiro_falso e ordenar_linhas
    exercicio = models.ForeignKey(Exercicio, on_delete=models.CASCADE, related_name='opcoes')
    texto = models.CharField(max_length=255)
    correta = models.BooleanField(default=False)
    ordem_correta = models.PositiveIntegerField(null=True, blank=True)  # só para "ordenar_linhas"


class ProgressoLicao(models.Model):
    usuario = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    licao = models.ForeignKey(Licao, on_delete=models.CASCADE)
    concluida = models.BooleanField(default=False)
    data_conclusao = models.DateTimeField(null=True, blank=True)

    class Meta:
        unique_together = ['usuario', 'licao']


class LiberacaoManual(models.Model):
    # registro de quando um professor libera um módulo travado manualmente
    usuario = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='liberacoes_recebidas')
    modulo = models.ForeignKey(Modulo, on_delete=models.CASCADE)
    liberado_por = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, related_name='liberacoes_concedidas')
    data = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ['usuario', 'modulo']


class PerfilGamificacao(models.Model):
    usuario = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    xp_total = models.PositiveIntegerField(default=0)
    streak_atual = models.PositiveIntegerField(default=0)
    streak_recorde = models.PositiveIntegerField(default=0)
    data_ultima_atividade = models.DateField(null=True, blank=True)

    @property
    def nivel_calculado(self):
        return self.xp_total // 100 + 1  # a cada 100 XP, sobe um nível


class TentativaExercicio(models.Model):
    usuario = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    exercicio = models.ForeignKey(Exercicio, on_delete=models.CASCADE)
    correta = models.BooleanField()
    data = models.DateTimeField(auto_now_add=True)


class ResultadoNivelamento(models.Model):
    # guarda o resultado do teste de nivelamento opcional (seção 4.4)
    usuario = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    trilha = models.ForeignKey(Trilha, on_delete=models.CASCADE)
    modulo_sugerido = models.ForeignKey(Modulo, on_delete=models.SET_NULL, null=True)
    modulo_confirmado_pelo_professor = models.ForeignKey(
        Modulo, on_delete=models.SET_NULL, null=True, related_name='+', blank=True
    )
    data = models.DateTimeField(auto_now_add=True)