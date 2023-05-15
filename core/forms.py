from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django_select2.forms import Select2Widget

from core.models import Visitante, TipoVisitante, SituacaoCadastro, FornecedorVisitante


class LoginForm(AuthenticationForm):
    error_messages = {
        'invalid_login': 'Usuário e/ou senha inválidos.',
    }


class VisitanteForm(forms.ModelForm):

    def clean_cpf(self):
        cpf = self.cleaned_data.get('cpf')
        if Visitante.objects.filter(cpf=cpf).exists():
            raise forms.ValidationError('CPF já cadastrado para outro usuário.')
        return cpf

    class Meta:
        model = Visitante
        fields = ['nome', 'cpf', 'id_tipovisitante', 'id_situacaocadastro']
        widgets = {
            'nome': forms.TextInput(attrs={'placeholder': 'Nome'}),
            'cpf': forms.TextInput(attrs={'type': 'number', 'placeholder': 'CPF'}),
        }

    id_tipovisitante = forms.ModelChoiceField(queryset=TipoVisitante.objects.all(), label='Tipo de Visitante')
    id_situacaocadastro = forms.ModelChoiceField(queryset=SituacaoCadastro.objects.all(), initial=SituacaoCadastro.objects.get(id=1), label='Situação de Cadastro')


class VisitanteUpdateForm(forms.ModelForm):
    id = forms.IntegerField(widget=forms.HiddenInput(), required=False)
    id_tipovisitante = forms.ModelChoiceField(queryset=TipoVisitante.objects.all(), label='Tipo de Visitante')
    id_situacaocadastro = forms.ModelChoiceField(queryset=SituacaoCadastro.objects.all(),
                                                 label='Situação de Cadastro')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['id'].widget.attrs['readonly'] = True

    class Meta:
        model = Visitante
        fields = ['id', 'nome', 'cpf', 'id_tipovisitante', 'id_situacaocadastro']
        field_order = ['id', 'nome', 'cpf', 'id_tipovisitante', 'id_situacaocadastro']
        widgets = {
            'nome': forms.TextInput(attrs={'placeholder': 'Nome'}),
            'cpf': forms.TextInput(attrs={'type': 'number', 'placeholder': 'CPF'})}


class FornecedorVisitanteForm(forms.ModelForm):

    class Meta:
        model = FornecedorVisitante
        fields = ['id_fornecedor', 'id_visitante']
        widgets = {
            'id_fornecedor': Select2Widget(
                attrs={
                    'data-placeholder': 'Selecionar Fornecedors',
                    'style': 'width: 100%;',
                    'data-minimum-input-length': 1
                }
            ),
            'id_visitante': Select2Widget(
                attrs={
                    'data-placeholder': 'Selecionar Visitante',
                    'style': 'width: 100%;',
                    'data-minimum-input-length': 1
                }
            ),
        }