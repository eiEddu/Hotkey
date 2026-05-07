from django import forms
from .models import Emprestimo
from clientes.models import Cliente
from reservas.models import Reserva

class EmprestimoQuartoForm(forms.ModelForm):
    cliente = forms.ModelChoiceField(queryset=Cliente.objects.all(), label="Cliente")
    reserva = forms.ModelChoiceField(
        queryset=Reserva.objects.filter(sala__tipo='QUARTO', status='ATIVA'),
        label="Reserva Ativa"
    )

    class Meta:
        model = Emprestimo
        fields = ['codigo', 'cliente', 'funcionario', 'reserva']

class EmprestimoSalaComercialForm(forms.ModelForm):
    cliente = forms.ModelChoiceField(queryset=Cliente.objects.all(), label="Cliente")
    reserva = forms.ModelChoiceField(
        queryset=Reserva.objects.filter(sala__tipo='SALA COMERCIAL', status='ATIVA'),
        label="Reserva Ativa"
    )

    class Meta:
        model = Emprestimo
        fields = ['codigo', 'cliente', 'funcionario', 'reserva']