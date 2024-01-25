
from django.contrib.auth.models import AbstractUser
from django.db import models

class Patient(AbstractUser):
    phone_number = models.CharField(max_length=15)

    def __str__(self):
        return self.username

class ReceiptPa(models.Model):
    patient = models.ForeignKey('Patients.Patient', on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateField(auto_now_add=True)
    psychologist = models.ForeignKey('Psychologists.Psychologist', on_delete=models.SET_NULL, null=True, blank=True)

class AppointmentPa(models.Model):
    patient = models.ForeignKey('Patients.Patient', on_delete=models.CASCADE)
    date = models.DateTimeField()
    description = models.TextField()
    psychologist = models.ForeignKey('Psychologists.Psychologist', on_delete=models.SET_NULL, null=True, blank=True)

class FeedbackPa(models.Model):
    patient = models.ForeignKey('Patients.Patient', on_delete=models.CASCADE)
    content = models.TextField()
    rating = models.PositiveIntegerField(default=0, choices=[(i, i) for i in range(1, 6)])  # Rating from 1 to 5
    created_at = models.DateTimeField(auto_now_add=True)
