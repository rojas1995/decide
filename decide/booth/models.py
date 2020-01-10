from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class profile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    edad = models.IntegerField(null=False)
    provincia = models.CharField(max_length=10, blank=False)
    municipio = models.CharField(default=None, max_length=20, blank=False)
    sexo = models.CharField(default=None, max_length=10, blank=False)

    class Meta:
        db_table = "auth_profile"