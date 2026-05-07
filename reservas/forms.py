from django import forms
from .models import Reserva
from salas.models import Sala

class ReservaQuartoForm(forms.ModelForm):
    sala = forms.ModelChoiceField(
        queryset=Sala.objects.filter(tipo='QUARTO', status='DISPONÍVEL'),
        label="Quarto Disponível"
    )

    class Meta:
        model = Reserva
        fields = '__all__'
        widgets = {
            'data_inicio': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            'data_fim': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        }
        error_messages = {
            'codigo': {'required': 'O código de reserva é obrigatório', 'unique': 'O código informado já existe'},
            'data_inicio': {'required': 'Data de início obrigatória'},
            'data_fim': {'required': 'Data fim obrigatória'}
        }

class ReservaSalaComercialForm(forms.ModelForm):
    sala = forms.ModelChoiceField(
        queryset=Sala.objects.filter(tipo='SALA COMERCIAL', status='DISPONÍVEL'),
        label="Sala Comercial Disponível"
    )

    class Meta:
        model = Reserva
        fields = '__all__'
        widgets = {
            'data_inicio': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            'data_fim': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        }
        error_messages = {
            'codigo': {'required': 'O código de reserva é obrigatório', 'unique': 'O código informado já existe'},
            'data_inicio': {'required': 'Data de início obrigatória'},
            'data_fim': {'required': 'Data fim obrigatória'}
        }