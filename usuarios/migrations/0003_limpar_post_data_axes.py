from django.db import migrations


def limpar_post_data(apps, schema_editor):
    """Apaga senhas digitadas que o axes gravou em texto puro (LGPD, minimização).

    Antes da correção em settings.py, a coluna post_data guardava o que foi
    digitado nas tentativas de login falhas, inclusive o campo de senha.
    Esta migração esvazia essa coluna em todas as linhas já existentes.
    """
    AccessAttempt = apps.get_model('axes', 'AccessAttempt')
    AccessAttempt.objects.exclude(post_data='').update(post_data='')


class Migration(migrations.Migration):

    dependencies = [
        ('usuarios', '0002_usuario_telefone'),
        # a tabela do axes precisa existir antes de limparmos
        ('axes', '0010_accessattemptexpiration'),
    ]

    operations = [
        # Não há como "desfazer" (as senhas não devem voltar), então o reverso não faz nada
        migrations.RunPython(limpar_post_data, migrations.RunPython.noop),
    ]