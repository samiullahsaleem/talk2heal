# psychologists/models.py
from django.contrib.auth.models import AbstractUser
from django.db import models

class Psychologist(AbstractUser):
    full_name = models.CharField(max_length=255)
    area = models.CharField(max_length=100)
    education = models.CharField(max_length=255)

    def __str__(self):
        return self.username

class SpecializationPs(models.Model):
    psychologist = models.ForeignKey('Psychologists.Psychologist', on_delete=models.CASCADE)
    field = models.CharField(max_length=100)

class ReceiptPs(models.Model):
    psychologist = models.ForeignKey('Psychologists.Psychologist', on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateField(auto_now_add=True)
    patient = models.ForeignKey('patients.Patient', on_delete=models.SET_NULL, null=True, blank=True)

class AppointmentPs(models.Model):
    psychologist = models.ForeignKey('Psychologists.Psychologist', on_delete=models.CASCADE)
    date = models.DateTimeField()
    description = models.TextField()
    patient = models.ForeignKey('Patients.Patient', on_delete=models.SET_NULL, null=True, blank=True)

class FeedbackPs(models.Model):
    psychologist = models.ForeignKey('Psychologists.Psychologist', on_delete=models.CASCADE)
    content = models.TextField()
    rating = models.PositiveIntegerField(default=0, choices=[(i, i) for i in range(1, 6)])  # Rating from 1 to 5
    created_at = models.DateTimeField(auto_now_add=True)
