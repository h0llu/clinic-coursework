from django.contrib import admin
from .models import Position, Employee, Schedule, Specialization,\
    Doctor, Office, Service, Patient, MedicalTest, Appointment


admin.site.register(Position)
admin.site.register(Employee)
admin.site.register(Schedule)
admin.site.register(Specialization)
admin.site.register(Doctor)
admin.site.register(Office)
admin.site.register(Service)
admin.site.register(Patient)
admin.site.register(MedicalTest)
admin.site.register(Appointment)
