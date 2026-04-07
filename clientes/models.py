from django.db import models

class Cliente(models.Model):
    CATEGORIA_CHOICES = [
        ('BRONZE', 'Bronze (1 Reserva)'),
        ('PRATA', 'Prata (2 Reservas)'),
        ('OURO', 'Ouro (3 Reservas)'),
    ]

    nome = models.CharField('Nome', max_length=100, help_text='Nome completo do cliente')
    cpf = models.CharField('CPF', max_length=14, unique=True, help_text='Apenas números ou formato 000.000.000-00')
    telefone = models.CharField('Telefone', max_length=20)
    categoria = models.CharField('Categoria', max_length=20, choices=CATEGORIA_CHOICES, default='BRONZE')

    class Meta:
        verbose_name = 'Cliente'
        verbose_name_plural = 'Clientes'

    def __str__(self):
        return f"{self.nome} - Categoria {self.get_categoria_display()}"