# patients/admin.py
from django.contrib import admin
from .models import Patient, ReceiptPa, AppointmentPa, FeedbackPa

admin.site.register(Patient)
admin.site.register(ReceiptPa)
admin.site.register(AppointmentPa)
admin.site.register(FeedbackPa)

