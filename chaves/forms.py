from django import forms

from chaves.models import Chave


class ChaveModelForm(forms.ModelForm):
    class Meta:
        model = Chave
        fields = '__all__'
        error_messages = {
            'codigo':{'required':'A identificação da chave é obrigatória'}
        }