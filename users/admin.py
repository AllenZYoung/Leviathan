from django.contrib import admin
from . import models

# Register your models here.
admin.site.register(models.Location)
admin.site.register(models.Hospital)
admin.site.register(models.Department)
admin.site.register(models.Doctor)
admin.site.register(models.DoctorDepartment)
admin.site.register(models.Bulletin)
admin.site.register(models.Adminreceptor)
admin.site.register(models.Adminpublisher)
admin.site.register(models.Appointment)
admin.site.register(models.Evaluation)
admin.site.register(models.Patient)