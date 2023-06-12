from django.db import models

from .models import Basic

# Create your models here.

class Defect(models.Model):
    defect = models.ForeignKey(Basic, on_delete=models.CASCADE)
    location = models.CharField(max_length=32)
    number = models.CharField(max_length=8)
    part = models.CharField(max_length=16)
    material = models.CharField(max_length=16)
    shapeType = models.CharField(max_length=32)
    width = models.CharField(max_length=8)
    LengthArea = models.CharField(max_length=8)
    each = models.CharField(max_length=8)
    progress = models.CharField(max_length=8)
    note = models.CharField(max_length=16)
    cause = models.CharField(max_length=32)
    photoNumber = models.CharField(max_length=16)
    photoName = models.CharField(max_length=32)