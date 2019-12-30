from django.db import models
from django.contrib.auth.models import User

class Perfil(models.Model):
    SEXOS = (
        ('M', 'Masculino'),
        ('F', 'Femenino')
    )

    user = models.OneToOneField(User, on_delete=models.CASCADE)

    sexo =  models.CharField(max_length=1, choices=SEXOS)
    edad = models.PositiveIntegerField()
    municipio = models.CharField(max_length=50)

    def __str__(self):
        return self.user.username
