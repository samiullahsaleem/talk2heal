from django.contrib import admin
from .models import Psychologist, Patient, Appointment, Payment
# Register your models here.
admin.site.register(Psychologist)
admin.site.register(Patient)
admin.site.register(Appointment)
admin.site.register(Payment)