from django.db import models

# Create your models here.
class Chave(models.Model):
    STATUS_CHOICES = [
        ('DISPONÍVEL', 'Disponível para empréstimo'),
        ('EMPRESTADA', 'Emprestada'),
        ('EXTRAVIADA', 'Perdida/Danificada'),
    ]

    TIPO_CHOICES = [
        ('BLOCO','Bloco'),
        ('Sala','Sala')
    ]

    codigo = models.CharField('Identificador',unique=True, max_length=100, help_text='Identificador da chave')
    tipo = models.CharField('Tipo', max_length=50, choices=TIPO_CHOICES, default='BLOCO')
    status = models.CharField('Status', max_length=50, choices=STATUS_CHOICES, default='DISPONÍVEL')

    class Meta:
        verbose_name = 'Chave'
        verbose_name_plural = 'Chaves'

    def __str__(self):
        return f"{self.codigo} - Status {self.get_status_display()} - Tipo {self.get_tipo_display()}"