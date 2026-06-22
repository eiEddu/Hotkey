from django import forms
from .models import Sala

from django import forms
from .models import Sala

# Form 1: Para Quartos (Não mostra o bloco)
class QuartoModelForm(forms.ModelForm):
    class Meta:
        model = Sala
        fields = ['nome','andar']
        error_messages = {
            'nome': {'required': 'Preencha o nome do quarto!'},
        }

# Form 2: Para Salas Comerciais (Mostra o bloco)
class SalaComercialModelForm(forms.ModelForm):
    class Meta:
        model = Sala
        fields = ['nome', 'bloco']
        error_messages = {
            'nome':{'required':'Preencha o nome da sala!'},
        }