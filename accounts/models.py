from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models
from utils.rands import random_letters
from django.utils.translation import gettext_lazy as _


class CustomUserManager(BaseUserManager):
    def create_user(self, email, password, **extra_fields):

        if not email:
            raise ValueError(_('O endereço de e-mail deve ser fornecido'))
        
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(self, email, password, **extra_fields):

        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_check', True)

        return self.create_user(email, password, **extra_fields)


class CustomUser(AbstractBaseUser, PermissionsMixin):

    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=30, blank=True, verbose_name=_('Nome'))
    last_name = models.CharField(max_length=30, blank=True, verbose_name=_('Sobrenome'))
    phone = models.CharField(max_length=20, verbose_name=_('Telefone'))
    token = models.CharField(max_length=6, default=random_letters(6))
    is_active = models.BooleanField(default=True, verbose_name=_('está ativo?'))
    is_staff = models.BooleanField(default=False, verbose_name=_("É da equipe?"))
    is_check = models.BooleanField(default=False, verbose_name=_("E-mail verificado?"))

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS:list[str] = []

    def __str__(self):
        return self.email
