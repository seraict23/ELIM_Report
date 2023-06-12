from django.contrib import admin

# Register your models here.
from .models import Basic, Contract, Facility, Worker, Map, UploadFile, PartPhoto, FMS_Usage, FacilityManagementStatus, Defect

admin.site.register(Basic)
admin.site.register(Contract)
admin.site.register(Facility)
admin.site.register(Worker)
admin.site.register(Map)
admin.site.register(UploadFile)
admin.site.register(PartPhoto)
admin.site.register(FMS_Usage)
admin.site.register(FacilityManagementStatus)

admin.site.register(Defect)
