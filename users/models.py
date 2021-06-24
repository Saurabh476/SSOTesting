from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.

# changes from stackoverflow 23-06-2021
# class User(AbstractUser):
#     access_token = models.CharField(max_length=2048, blank=True, null=True)
#     id_token = models.CharField(max_length=2048, blank=True, null=True)
#     token_expires = models.DateTimeField(blank=True, null=True)

