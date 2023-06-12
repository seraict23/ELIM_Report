from django.db import models
from .models import Basic



class FacilityManagementStatus(models.Model):
    facilityManagementStatus = models.ForeignKey(Basic, on_delete=models.CASCADE)
    FMS_Usage = models.CharField(max_length=8)
    FMS_Structure = models.CharField(max_length=8)
    FMS_Env = models.CharField(max_length=8)
    FMS_Expansion = models.CharField(max_length=8)
    FMS_Overload = models.CharField(max_length=8)
    FMS_Accident = models.CharField(max_length=8)


class FMS_Usage(models.Model):
    basic = models.ForeignKey(Basic, on_delete=models.CASCADE)
    floor = models.CharField(max_length=32)
    before_useFor = models.CharField(max_length=32)
    before_area = models.CharField(max_length=32)
    after_useFor = models.CharField(max_length=32)
    after_area = models.CharField(max_length=32)
    date = models.CharField(max_length=32)
    note = models.CharField(max_length=32)

class FMS_Usage_Photo(models.Model):
    FMS_Usage_Photo = models.ForeignKey(FMS_Usage, on_delete=models.CASCADE)
    name = models.CharField(max_length=32)
    path = models.CharField(max_length=32)

class FMS_Structure(models.Model):
    basic = models.ForeignKey(Basic, on_delete=models.CASCADE)
    wing = models.CharField(max_length=32)
    material = models.CharField(max_length=32)
    mark = models.CharField(max_length=32)
    location = models.CharField(max_length=32)
    content = models.CharField(max_length=32)
    personInCharge = models.CharField(max_length=32)
    date = models.CharField(max_length=32)

class FMS_Structure_Photo(models.Model):
    FMS_Structure_Photo = models.ForeignKey(FMS_Structure, on_delete=models.CASCADE)
    name = models.CharField(max_length=32)
    path = models.CharField(max_length=32)

class FMS_Env(models.Model):
    basic = models.ForeignKey(Basic, on_delete=models.CASCADE)
    # type = models.CharField(max_length=32)
    location = models.CharField(max_length=32)
    before = models.CharField(max_length=32)
    after = models.CharField(max_length=32)


class FMS_Env_Photo(models.Model):
    FMS_Env_Photo = models.ForeignKey(FMS_Env, on_delete=models.CASCADE)
    name = models.CharField(max_length=32)
    path = models.CharField(max_length=32)

class FMS_Expansion(models.Model):
    basic = models.ForeignKey(Basic, on_delete=models.CASCADE)
    floor = models.CharField(max_length=32)
    before_useFor = models.CharField(max_length=32)
    before_area = models.CharField(max_length=32)
    after_useFor = models.CharField(max_length=32)
    after_area = models.CharField(max_length=32)
    date = models.CharField(max_length=32)
    note = models.CharField(max_length=32)


class FMS_Expansion_Photo(models.Model):
    FMS_Expansion_Photo = models.ForeignKey(FMS_Expansion, on_delete=models.CASCADE)
    name = models.CharField(max_length=32)
    path = models.CharField(max_length=32)

class FMS_Overload(models.Model):
    basic = models.ForeignKey(Basic, on_delete=models.CASCADE)
    type = models.CharField(max_length=32)
    location = models.CharField(max_length=32)
    text = models.CharField(max_length=128)
    note = models.CharField(max_length=32)

class FMS_Overload_Photo(models.Model):
    FMS_Overload_Photo = models.ForeignKey(FMS_Overload, on_delete=models.CASCADE)
    name = models.CharField(max_length=32)
    path = models.CharField(max_length=32)

class FMS_Accident(models.Model):
    basic = models.ForeignKey(Basic, on_delete=models.CASCADE)
    title = models.CharField(max_length=32)
    content = models.TextField()
    location = models.CharField(max_length=32)
    degree_of_damage = models.CharField(max_length=32)
    action = models.CharField(max_length=32)
    status = models.CharField(max_length=32)


class FMS_Accident_Photo(models.Model):
    FMS_Accident_Photo = models.ForeignKey(FMS_Accident, on_delete=models.CASCADE) 
    name = models.CharField(max_length=32)
    path = models.CharField(max_length=32)