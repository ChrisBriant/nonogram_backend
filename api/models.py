from django.db import models
from django.contrib.postgres.fields import ArrayField
from django.contrib.auth.models import User

# Create your models here.
class Nonogram(models.Model):
    word = models.CharField(null=False, max_length=9)
    combos = ArrayField(models.CharField(max_length=9, blank=True))

class ApiKey(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    key = models.CharField(null=False,max_length=128)


