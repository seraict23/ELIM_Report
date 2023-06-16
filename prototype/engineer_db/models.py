from django.db import models

# Create your models here.

class Engineer(models.Model):
    engineer_name = models.CharField(max_length=32)
    birth = models.DateField()
    start_workAt = models.DateField()

    def __str__(self):
        return self.engineer_name

class Job(models.Model):
    engineers = models.ManyToManyField(Engineer)
    job_name = models.CharField(max_length=128)
    client = models.CharField(max_length=64)
    startAt = models.DateField(auto_created=False)
    finishAt = models.DateField(auto_created=False)
    work_days = models.IntegerField()
    money = models.IntegerField()
    category = models.CharField(max_length=32)

    def __str__(self):
        return self.job_name