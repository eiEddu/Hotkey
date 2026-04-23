from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models


class Bloco(models.Model):

    ANDAR_CHOICES = [
        ('1', 'Primeiro Andar'),
        ('2', 'Segundo Andar'),
        ('3', 'Terceiro Andar'),
    ]

    codigo = models.CharField('Codigo',max_length=100, unique=True, help_text='Identificador do bloco')
    andar = models.CharField('Andar',max_length=100, choices=ANDAR_CHOICES, help_text='Andar do bloco',default='1')
    quantidade = models.IntegerField('Quantidade',validators=[MinValueValidator(0), MaxValueValidator(15)],help_text='Quantidade de salas do bloco(Máx: 15)')

    class Meta:
        verbose_name = 'Bloco'
        verbose_name_plural = 'Blocos'

    def __str__(self):
        return f"{self.codigo} - Andar {self.get_andar_display()}"