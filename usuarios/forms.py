from django import forms
from django.contrib.auth.forms import UserCreationForm

from .models import Usuario


class CadastroForm(UserCreationForm):
    """
    Formulario de cadastro de novos usuarios.

    Estende o UserCreationForm do Django: a senha e digitada duas vezes
    e passa pelos validadores configurados em AUTH_PASSWORD_VALIDATORS.
    O login do Nivela e por e-mail, entao so pedimos o e-mail e
    preenchemos o username (ainda obrigatorio no modelo) com o mesmo valor.
    """

    # Consentimento explícito aos Termos de Uso / Política de Privacidade
    # (item 4.4 do checklist LGPD). Vem desmarcado por padrão e é
    # obrigatório: o cadastro não é concluído sem essa ação afirmativa.
    aceite_termos = forms.BooleanField(
        label='Li e aceito os Termos de Uso e a Política de Privacidade',
        required=True,
    )

    class Meta:
        model = Usuario
        fields = ('email',)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['email'].label = 'Endereço de e-mail'
        self.fields['password1'].label = 'Senha'
        self.fields['password2'].label = 'Confirmar senha'
        # Mesmo visual dos campos da tela de login (Bootstrap)
        for nome, field in self.fields.items():
            if nome == 'aceite_termos':
                field.widget.attrs['class'] = 'form-check-input'
            else:
                field.widget.attrs['class'] = 'form-control'

    def save(self, commit=True):
        user = super().save(commit=False)
        # username continua existindo no banco, mas nao e usado para login
        user.username = self.cleaned_data['email']
        if commit:
            user.save()
        return user