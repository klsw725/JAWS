from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Images(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='%(class)s', null=True)
    name = models.CharField(max_length=100, null=False, blank=False)
    image = models.ImageField(blank=False, null=True)
    encoding = models.FileField(null=True, blank=True)

class Device(models.Model):
    owner = models.ForeignKey(User,  on_delete=models.SET_NULL, null=True, related_name='%(class)s')
    devicecode = models.CharField(max_length=6, null=False, blank=False)
