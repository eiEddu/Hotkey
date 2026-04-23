from django.db import models

import chaves.models
import clientes.models
import reservas.models


class Emprestimo(models.Model):
    STATUS_CHOICES = [
        ('ATIVO','Ativo'),
        ('FINALIZADO/DEVOLVIDO','Finalizado/Devolvido')
    ]

    codigo = models.CharField('Codigo', max_length=100,unique=True, help_text='Codigo do empréstimo')
    data_inicio = models.DateTimeField('Data de Inicio',help_text='Data de Inicio do empréstimo')
    data_devolucao = models.DateTimeField('Data de devolucao',help_text='Data de devolução')
    reserva = models.ForeignKey(reservas.models.Reserva,verbose_name='Reserva',help_text='Código da reserva',on_delete=models.PROTECT,related_name='reserva')
    cliente = models.ForeignKey(clientes.models.Cliente,verbose_name='Cliente',help_text='Nome do Cliente',on_delete=models.PROTECT,related_name='emprestimo_cliente')
    chave = models.ForeignKey(chaves.models.Chave,verbose_name='Chave',help_text='Código da Chave',on_delete=models.PROTECT,related_name='chave')
    status = models.CharField('Status',max_length=50,choices=STATUS_CHOICES,default='ATIVO')
