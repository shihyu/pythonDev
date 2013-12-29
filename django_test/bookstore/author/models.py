from django.db import models

# Create your models here.
class Profile(models.Model):
    name     = models.CharField(max_length = 50)
    age      = models.IntegerField()
    tel      = models.CharField(max_length = 30)
    address  = models.CharField(max_length = 100)
    email    = models.EmailField()
