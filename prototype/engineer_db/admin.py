from django.contrib import admin

# Register your models here.
from .models import Engineer, Job

admin.site.register(Engineer)
admin.site.register(Job)
