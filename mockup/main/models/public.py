from django.db import models
from .models import Basic

# Create your models here.


class Public(models.Model):
    public = models.ForeignKey(Basic, on_delete=models.CASCADE)
    handrail_grade = models.CharField(max_length=8, default="")
    handrail_inpection = models.TextField(default="")
    handrail_photoA = models.CharField(max_length=128, default="")
    handrail_photoB = models.CharField(max_length=128, default="")
    roadJoint_grade = models.CharField(max_length=8, default="")
    roadJoint_inpection = models.TextField(default="")
    roadJoint_photoA = models.CharField(max_length=128, default="")
    roadJoint_photoB = models.CharField(max_length=128, default="")
    pavement_grade = models.CharField(max_length=8, default="")
    pavement_inpection = models.TextField(default="")
    pavement_photoA = models.CharField(max_length=128, default="")
    pavement_photoB = models.CharField(max_length=128, default="")
    ventCover_grade = models.CharField(max_length=8, default="")
    ventCover_inpection = models.TextField(default="")
    ventCover_photoA = models.CharField(max_length=128, default="")
    ventCover_photoB = models.CharField(max_length=128, default="")
    exterior_inpection = models.TextField(default="")
    exterior_photoA = models.CharField(max_length=128, default="")
    exterior_photoB = models.CharField(max_length=128, default="")
    exterior_photoC = models.CharField(max_length=128, default="")
    exterior_photoD = models.CharField(max_length=128, default="")
    exterior_photoE = models.CharField(max_length=128, default="")
    exterior_photoF = models.CharField(max_length=128, default="")
    exterior_photoG = models.CharField(max_length=128, default="")
    exterior_photoH = models.CharField(max_length=128, default="")
    exterior_photoI = models.CharField(max_length=128, default="")
    exterior_photoJ = models.CharField(max_length=128, default="")
