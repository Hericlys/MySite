from django.db import models
from accounts.models import CustomUser as User
from django.utils.translation import gettext_lazy as _


class Budget(models.Model):
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    category = models.CharField(max_length=50, verbose_name=_('Categoria'))
    description = models.TextField(verbose_name=_('Descrição'))
    STATUS_CHOICES = [
        ('Recebido', _('Recebido')),
        ('Contatado', _('Contatado')),
        ('Aceito', _('Aceito')),
        ('Finalizado', _('Finalizado')),
    ]
    status = models.CharField(
        max_length=50,
        choices=STATUS_CHOICES,
        default=STATUS_CHOICES[0]
    )
    request_date = models.DateField(auto_now_add=True, verbose_name=_('Data da solicitação'))
    contacted_date = models.DateField(auto_now=True, verbose_name=_('Data do contato'))
    contact_attempts = models.IntegerField(default=0, verbose_name=_('Tentativa de contato'))
    established_contact = models.BooleanField(
        default=False,
        help_text=_("Marque essa opção apenas se conseguiu contato com o cliente"),
        verbose_name=_('Contato realizado?')
    )

    def __str__(self) -> str:
        return _(f'Orçamento de {self.user}')
