from django.db import models
from django.core.exceptions import ValidationError
import clientes.models
import funcionarios.models
import salas.models


class Reserva(models.Model):
    STATUS_CHOICES = [
        ('ATIVA', 'Ativa'),
        ('ENCERRADA', 'Encerrada'),
        ('CANCELADA', 'Cancelada'),
    ]
    codigo = models.CharField('Codigo', max_length=100, unique=True, help_text='Codigo da reserva')
    data_inicio = models.DateTimeField('Data de início', help_text='Data de início da reserva')
    data_fim = models.DateTimeField('Data de fim', help_text='Data de fim da reserva')
    status = models.CharField('Status', max_length=50, choices=STATUS_CHOICES, default='ATIVA')
    cliente = models.ForeignKey(clientes.models.Cliente, verbose_name='Cliente', help_text='Nome do Cliente',
                                on_delete=models.PROTECT, related_name='reserva_cliente')
    sala = models.ForeignKey(salas.models.Sala, verbose_name='Sala', help_text='Nome da Sala', on_delete=models.PROTECT,
                             related_name='sala')
    funcionario = models.ForeignKey(funcionarios.models.Funcionario, verbose_name='Funcionário',
                                    help_text='Nome do Funcionário', on_delete=models.PROTECT,
                                    related_name='funcionario')

    class Meta:
        verbose_name = 'Reserva'
        verbose_name_plural = 'Reservas'

    def clean(self):
        super().clean()

        if self.cliente:
            reservas_ativas = Reserva.objects.filter(
                cliente=self.cliente,
                status='ATIVA'
            ).exclude(pk=self.pk).count()

            limites = {
                'BRONZE': 1,
                'PRATA': 2,
                'OURO': 3
            }
            limite_cliente = limites.get(self.cliente.categoria, 1)
            if reservas_ativas >= limite_cliente:
                raise ValidationError({
                    'cliente': f"Bloqueio: Este cliente possui a categoria {self.cliente.get_categoria_display()} e já atingiu o limite de {limite_cliente} reserva(s) ativa(s)."
                })


        if self.data_inicio and self.data_fim:

            if self.data_inicio >= self.data_fim:
                raise ValidationError({
                    'data_fim': 'A data de término deve ser posterior à data de início.'
                })

            conflitos = Reserva.objects.filter(
                sala=self.sala,
                status='ATIVA',
                data_inicio__lt=self.data_fim,
                data_fim__gt=self.data_inicio
            ).exclude(pk=self.pk)

            if conflitos.exists():
                raise ValidationError({
                    'data_inicio': f"A sala/quarto {self.sala.codigo} já está ocupada neste período.",
                    'data_fim': "Por favor, escolha outros horários."
                })

    def __str__(self):
        return f"{self.codigo} - Cliente: {self.cliente.nome} - Sala: {self.sala.codigo}"
