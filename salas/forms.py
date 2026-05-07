from django import forms
from .models import Sala

from django import forms
from .models import Sala

# Form 1: Para Quartos (Não mostra o bloco)
class QuartoModelForm(forms.ModelForm):
    class Meta:
        model = Sala
        fields = ['codigo', 'status']
        error_messages = {
            'codigo': {'required':'O identificador da sala é obrigatório', 'unique':'O identificador informado já existe'}
        }

# Form 2: Para Salas Comerciais (Mostra o bloco)
class SalaComercialModelForm(forms.ModelForm):
    class Meta:
        model = Sala
        fields = ['codigo', 'status', 'bloco']
        error_messages = {
            'codigo': {'required':'O identificador da sala é obrigatório', 'unique':'O identificador informado já existe'}
        }