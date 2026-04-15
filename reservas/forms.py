from django import forms
from reservas.models import Reserva


class ReservaModelForm(forms.ModelForm):
    class Meta:
        model = Reserva
        fields = '__all__'
        error_messages = {
            'codigo':{'required':'O código de reserva é obrigatório','unique':'O código informado já existe'},
            'data_inicio':{'required':'Data de início obrigatória'},
            'data_fim': {'required': 'Data fim obrigatória'}
        }