from django import forms

from .models import Sala


class SalaModelForm(forms.ModelForm):
    class Meta:
        model = Sala
        fields = '__all__'
        error_messages = {
            'codigo':{'required':'O identificador da sala é obrigatório','unique':'O identificador informado já existe'}
        }