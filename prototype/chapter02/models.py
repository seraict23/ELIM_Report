from django.db import models
from common.models import Common

# Create your models here.

class UsageChange(models.Model):
    STATUS_CHOICES = (
        (1, 'YES'),
        (2, 'NO'),
        (3, 'UNKNOWN'),
    )
    building = models.ForeignKey(Common, on_delete=models.CASCADE)
    existence = models.IntegerField(choices = STATUS_CHOICES)
    floor = models.CharField(max_length=32)
    before_useFor = models.CharField(max_length=32)
    before_area = models.CharField(max_length=32)
    after_useFor = models.CharField(max_length=32)
    after_area = models.CharField(max_length=32)
    date = models.DateField()
    note = models.CharField(max_length=32)


class StructureChange(models.Model):
    STATUS_CHOICES = (
        (1, 'YES'),
        (2, 'NO'),
        (3, 'UNKNOWN'),
    )
    building = models.ForeignKey(Common, models.CASCADE)
    existence = models.IntegerField(choices = STATUS_CHOICES)
    wing = models.CharField(max_length=32)
    material = models.CharField(max_length=32)
    mark = models.CharField(max_length=32)
    location = models.CharField(max_length=32)
    content = models.CharField(max_length=32)
    personInCharge = models.CharField(max_length=32)



class EnvironmentChange(models.Model):
    STATUS_CHOICES = (
        (1, 'YES'),
        (2, 'NO'),
        (3, 'UNKNOWN'),
    )
    building = models.ForeignKey(Common, models.CASCADE)
    existence = models.IntegerField(choices = STATUS_CHOICES)
    type = models.CharField(max_length=32)
    location = models.CharField(max_length=32)
    before = models.CharField(max_length=32)
    after = models.CharField(max_length=32)


class Expansion(models.Model):
    STATUS_CHOICES = (
        (1, 'YES'),
        (2, 'NO'),
        (3, 'UNKNOWN'),
    )
    building = models.ForeignKey(Common, models.CASCADE)
    existence = models.IntegerField(choices = STATUS_CHOICES)
    floor = models.CharField(max_length=32)
    before_useFor = models.CharField(max_length=32)
    before_area = models.CharField(max_length=32)
    after_useFor = models.CharField(max_length=32)
    after_area = models.CharField(max_length=32)
    date = models.DateField()
    note = models.CharField(max_length=32)



class Overload(models.Model):
    STATUS_CHOICES = (
        (1, 'YES'),
        (2, 'NO'),
        (3, 'UNKNOWN'),
    )
    building = models.ForeignKey(Common, models.CASCADE)
    existence = models.IntegerField(choices = STATUS_CHOICES)
    floor = models.CharField(max_length=32)
    before_useFor = models.CharField(max_length=32)
    before_area = models.CharField(max_length=32)
    after_useFor = models.CharField(max_length=32)
    after_area = models.CharField(max_length=32)
    date = models.DateField()


class Accident(models.Model):
    STATUS_CHOICES = (
        (1, 'YES'),
        (2, 'NO'),
        (3, 'UNKNOWN'),
    )
    building = models.ForeignKey(Common, models.CASCADE)
    existence = models.IntegerField(choices = STATUS_CHOICES)
    title = models.CharField(max_length=32)
    content = models.TextField()
    location = models.CharField(max_length=32)
    degree_of_damage = models.CharField(max_length=32)
    action = models.CharField(max_length=32)
    status = models.CharField(max_length=32)



class Pictures_CH02(models.Model):
    FACTION_CHOICES = [
        ('UsageChange', '용도변경'),
        ('StructureChange', '구조변경'),
        ('EnvironmentChange', '주변조건의 변경사항'),
        ('Expansion', '증개축'),
        ('Overload', '과하중'),
        ('Accident', '사고'),
    ]

    building = models.ForeignKey(Common, models.CASCADE)
    faction = models.CharField(choices=FACTION_CHOICES, max_length=32)
    pictureName = models.CharField(max_length=64)
    picturePath = models.TextField()