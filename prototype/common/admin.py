from django.contrib import admin

# Register your models here.


from .models import Common, Worker

admin.site.register(Common)
admin.site.register(Worker)
