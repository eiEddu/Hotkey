from django.db import models


class Sala(models.Model):

    TIPO_CHOICES = [
        ('QUARTO', 'Quarto'),
        ('SALA COMERCIAL','Sala Comercial')
    ]

    STATUS_CHOICES = [
        ('DISPONÍVEL','Disponível para reserva'),
        ('RESERVADA','Reservada')
    ]

    ANDAR_CHOICES = [
        ('1', 'Primeiro Andar'),
        ('2', 'Segundo Andar'),
        ('3', 'Terceiro Andar'),
        ('4', 'Quarto Andar'),
        ('5', 'Quinto Andar'),
        ('6', 'Sexto Andar'),
        ('7', 'Setimo Andar'),
        ('8', 'Oitavo Andar'),
    ]

    codigo = models.CharField('Codigo', max_length=100,help_text='Identificador da sala')
    tipo = models.CharField('Tipo', max_length=50, choices=TIPO_CHOICES, default='QUARTO')
    status = models.CharField('Status',max_length=50,choices=STATUS_CHOICES,help_text='Status da sala',default='DISPONÍVEL')
    andar = models.CharField('Andar',max_length=50,choices=ANDAR_CHOICES,null=True, blank=True)
    bloco = models.ForeignKey('blocos.Bloco', on_delete=models.PROTECT, null=True, blank=True)


    class Meta:
        verbose_name = 'Sala'
        verbose_name_plural = 'Salas'

    def __str__(self):
        return f"{self.codigo}"