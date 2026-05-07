from django.db import models
import chaves.models
import clientes.models
import reservas.models
import funcionarios.models

class Emprestimo(models.Model):
    STATUS_CHOICES = [
        ('ATIVO','Ativo'),
        ('FINALIZADO/DEVOLVIDO','Finalizado/Devolvido')
    ]

    codigo = models.CharField('Codigo', max_length=100, unique=True)
    data_inicio = models.DateTimeField('Data de Inicio')
    data_devolucao = models.DateTimeField('Data de Devolução')
    reserva = models.ForeignKey(reservas.models.Reserva, on_delete=models.PROTECT, related_name='emprestimo_reserva')
    cliente = models.ForeignKey(clientes.models.Cliente, on_delete=models.PROTECT, related_name='emprestimo_cliente')
    funcionario = models.ForeignKey(funcionarios.models.Funcionario, on_delete=models.PROTECT,related_name='emprestimo_funcionario', verbose_name='Funcionário',help_text='Funcionário que entregou a chave', null=True, blank=True)
    chave = models.ForeignKey(chaves.models.Chave, verbose_name='Chave da Sala/Quarto', on_delete=models.PROTECT, related_name='emprestimo_chave')
    chave_bloco = models.ForeignKey(chaves.models.Chave, verbose_name='Chave do Bloco', on_delete=models.PROTECT, null=True, blank=True, related_name='emprestimo_chave_bloco')
    status = models.CharField('Status', max_length=50, choices=STATUS_CHOICES, default='ATIVO')

    class Meta:
        verbose_name = 'Empréstimo'
        verbose_name_plural = 'Empréstimos'

    def __str__(self):
        return f"{self.codigo}"