from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Images(models.Model):
    # owner = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100, null=False, blank=False)
    image = models.ImageField(blank=False, null=False)

