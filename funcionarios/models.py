from django.db import models

from clientes.models import Pessoa


class Funcionario(Pessoa):
    CARGO_CHOICES = [
        ('PORTEIRO', 'Porteiro'),
        ('GERENTE', 'Gerente'),
    ]

    cargo = models.CharField ('Cargo',max_length=20, choices=CARGO_CHOICES, default='PORTEIRO')

    class Meta:
        verbose_name = 'Funcionario'
        verbose_name_plural = 'Funcionarios'

    def __str__(super):
        return f"{super.nome} - Cargo {super.get_cargo_display()}"