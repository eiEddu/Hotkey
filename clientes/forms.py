from django import forms
from .models import Cliente

class ClienteModelForm(forms.ModelForm):
    class Meta:
        model = Cliente
        fields = '__all__'
        error_messages = {
            'nome': {'required': 'O nome do cliente é obrigatório.'},
            'cpf': {'required': 'O CPF é obrigatório.', 'unique': 'Este CPF já está cadastrado.'},
            'telefone':{'required': 'o Telefone do cliente é obrigatório'}
        }