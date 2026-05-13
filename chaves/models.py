from django.db import models

class Chave(models.Model):
    STATUS_CHOICES = [
        ('DISPONÍVEL', 'Disponível para empréstimo'),
        ('EMPRESTADA', 'Emprestada'),
        ('EXTRAVIADA', 'Perdida/Danificada'),
    ]
    TIPO_CHOICES = [
        ('BLOCO','Bloco'),
        ('SALA','Sala')
    ]

    codigo = models.CharField('Identificador', max_length=100)
    tipo = models.CharField('Tipo', max_length=50, choices=TIPO_CHOICES, default='BLOCO')
    status = models.CharField('Status', max_length=50, choices=STATUS_CHOICES, default='DISPONÍVEL')
    bloco = models.ForeignKey('blocos.Bloco', on_delete=models.PROTECT, null=True, blank=True)
    sala = models.ForeignKey('salas.Sala', on_delete=models.PROTECT, null=True, blank=True)

    class Meta:
        verbose_name = 'Chave'
        verbose_name_plural = 'Chaves'

    def __str__(self):
        return f"{self.codigo}"