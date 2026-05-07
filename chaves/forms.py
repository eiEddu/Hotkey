from django import forms
from .models import Chave
from salas.models import Sala  # Precisamos importar o model Sala para filtrar!


# 1. Form de Bloco
class ChaveBlocoModelForm(forms.ModelForm):
    class Meta:
        model = Chave
        fields = ['codigo', 'status', 'bloco']

# 2. Form de Quarto
class ChaveQuartoModelForm(forms.ModelForm):
    sala = forms.ModelChoiceField(
        queryset=Sala.objects.filter(tipo='QUARTO'),
        label="Quarto"
    )
    class Meta:
        model = Chave
        fields = ['codigo', 'status', 'sala']


# 3. Form de Sala Comercial
class ChaveSalaComercialModelForm(forms.ModelForm):
    sala = forms.ModelChoiceField(
        queryset=Sala.objects.filter(tipo='SALA COMERCIAL'),
        label="Sala Comercial"
    )

    class Meta:
        model = Chave
        fields = ['codigo', 'status', 'sala']