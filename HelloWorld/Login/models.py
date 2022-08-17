from django.db import models


class User(models.Model):
    username = models.CharField(max_length=50)
    password= models.CharField(max_length=50)
    isAdmin=models.BooleanField()
    account=models.CharField(max_length=9)