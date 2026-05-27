from django import forms

from .models import Bloco


class BlocoModelForm(forms.ModelForm):
    class Meta:
        model = Bloco
        fields = ['andar','quantidade']
        error_messages = {
            'quantidade':{'required':'Insira a quantidade de salas registradas no bloco!',}
        }