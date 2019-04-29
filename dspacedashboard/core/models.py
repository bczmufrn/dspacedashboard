import uuid

from django.db import models

class BaseModel(models.Model):
	id = models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True)
	created_at = models.DateTimeField('Criado em', auto_now_add=True)
	updated_at = models.DateTimeField('Atualizado em', auto_now=True)

	class Meta:
		abstract = True
