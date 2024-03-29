import re

from django.db import models
from django.db.models import Q
from django.core import validators
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, UserManager
from django.conf import settings

from dspacedashboard.core.models import BaseModel

class CustomUserManager(UserManager):
	def search(self, query):
		return self.filter(Q(name__icontains=query) | Q(username__icontains=query) | Q(email__icontains=query))

class User(BaseModel, AbstractBaseUser, PermissionsMixin):
	username = models.CharField(
		'Login', max_length=30, unique=True,
		validators=[validators.RegexValidator(re.compile('^[\w.@+-]+$'),
			'O nome de usuário so pode conter letras, digitos ou os seguintes caracteres: @/./+/-/_', 'invalid')]
	)
	email = models.EmailField('E-mail', blank=True)
	name = models.CharField('Nome', max_length=100, blank=True)	
	is_active = models.BooleanField('Está ativo', blank=True, default=True)
	is_staff = models.BooleanField('Administrador', blank=True, default=False)

	objects = CustomUserManager()

	USERNAME_FIELD = 'username'
	REQUIRED_FIELDS = ['email']

	def __str__(self):
		return self.name or self.username

	def get_short_name(self):
		return self.username

	def get_full_name(self):
		return str(self)

	class Meta:
		verbose_name='Usuário'
		verbose_name_plural='Usuários'