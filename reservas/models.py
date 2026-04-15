from tabnanny import verbose
from django.db import models

import clientes.models
import funcionarios.models
import salas.models


class Reserva(models.Model):
    STATUS_CHOICES = [
        ('ATIVA','Ativa'),
        ('ENCERRADA','Encerrada')
    ]
    codigo = models.CharField('Codigo', max_length=100,unique=True, help_text='Codigo da reserva')
    data_inicio = models.DateTimeField('Data de início',help_text='Data de início da reserva')
    data_fim = models.DateTimeField('Data de fim',help_text='Data de fim da reserva')
    status = models.CharField('Status',max_length=50,choices=STATUS_CHOICES,default='ATIVA')
    cliente = models.ForeignKey(clientes.models.Cliente,verbose_name='Cliente',help_text='Nome do Cliente',on_delete=models.PROTECT,related_name='cliente')
    sala = models.ForeignKey(salas.models.Sala, verbose_name='Sala',help_text='Nome do Cliente',on_delete=models.PROTECT,related_name='sala')
    funcionario = models.ForeignKey(funcionarios.models.Funcionario,verbose_name='Funcionário',help_text='Nome do Funcionário',on_delete=models.PROTECT,related_name='funcionario')

    class Meta:
        verbose_name = 'Reserva'
        verbose_name_plural = 'Reservas'

    def __str__(self):
        return f"{self.codigo} - Status {self.get_status_display()}"