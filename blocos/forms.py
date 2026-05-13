from django import forms

from .models import Bloco


class BlocoModelForm(forms.ModelForm):
    class Meta:
        model = Bloco
        fields = ['andar','quantidade']
        error_messages = {
            'codigo':{'required':'O Código do bloco é obrigatório','unique':'O código já foi cadastrado'}
        }