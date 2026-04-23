from django import forms

from emprestimos.models import Emprestimo


class EmprestimoModelForm(forms.ModelForm):
    class Meta:
        model = Emprestimo
        fields = '__all__'
        error_messages = {
            'codigo': {'required':'o Codigo de empréstimo é obrigatorio','unique':'o código de empréstimo já existe'},
            'data_inicio': {'required': 'Data de início obrigatória'}
        }