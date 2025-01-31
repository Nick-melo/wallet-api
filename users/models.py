from django.contrib.auth.models import User
from django.db import models

class Profile(models.Model):  # Exemplo se precisar de mais dados no usuário
    user = models.OneToOneField(User, on_delete=models.CASCADE)

