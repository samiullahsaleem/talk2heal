# psychologists/admin.py
from django.contrib import admin
from .models import Psychologist, SpecializationPs, ReceiptPs, AppointmentPs, FeedbackPs

admin.site.register(Psychologist)
admin.site.register(SpecializationPs)
admin.site.register(ReceiptPs)
admin.site.register(AppointmentPs)
admin.site.register(FeedbackPs)


