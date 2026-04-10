from django import forms
from funcionarios.models import Funcionario


class FuncionarioModelForm(forms.ModelForm):
    class Meta:
        model = Funcionario
        fields = '__all__'
        error_messages = {
            'nome':{'required':'O nome do funcionário é obrigatório'},
            'cpf' :{'required': 'O CPF do funcionário é obrigatório'}
        }