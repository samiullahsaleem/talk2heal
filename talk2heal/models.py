from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone

from cloudinary.models import CloudinaryField
class Psychologist(models.Model):
    username = models.CharField(max_length=255, default='')
    city = models.CharField(max_length=255, default='')
    email = models.EmailField(max_length=255, default='')
    password = models.CharField(max_length=255, default='')
    name = models.CharField(max_length=255, default='')
    profile_picture = CloudinaryField('image', null=True, blank=True)
    rate = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)
    years_of_experience = models.PositiveIntegerField(default=0)
    degree = models.CharField(max_length=255, default='')
    contact_number = models.CharField(max_length=15, default='')
    address = models.TextField(default='')
    account_verified_status = models.CharField(
        max_length=20,
        choices=[('pending', 'Pending'), ('failed', 'Failed'), ('verified', 'Verified')],
        default='pending'
    )
    rating = models.DecimalField(max_digits=3, decimal_places=2, default=0.0)
    
    groups = models.ManyToManyField(
        'auth.Group',
        related_name='psychologists',
        blank=True
    )
    
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='psychologists_permissions',
        blank=True
    )

    def __str__(self):
        return self.username

class Patient(models.Model):
    username = models.CharField(max_length=255, default='')
    email = models.EmailField(max_length=255, default='')
    password = models.CharField(max_length=255, default='')
    name = models.CharField(max_length=255, default='')
    profile_picture =     profile_picture = CloudinaryField('image', null=True, blank=True)
    contact_number = models.CharField(max_length=15, default='')
    address = models.TextField(default='')
    city = models.CharField(max_length=255, default='')
    groups = models.ManyToManyField(
        'auth.Group',
        related_name='patients',
        blank=True
    )
    
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='patients_permissions',
        blank=True
    )

    def __str__(self):
        return self.username

class Appointment(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    psychologist = models.ForeignKey(Psychologist, on_delete=models.CASCADE)
    appointment_date = models.DateTimeField()
    time_slot = models.CharField(max_length=255, default='')
    is_paid = models.BooleanField(default=False)
    payment_date = models.DateTimeField(null=True, blank=True)
    chat_enabled = models.BooleanField(default=False)
    chat_link = models.CharField(max_length=100, blank=True, null=True)
    location = models.CharField(max_length=255, default='')

    def __str__(self):
        return f"{self.patient} - {self.psychologist} - {self.appointment_date}"

class Payment(models.Model):
    appointment = models.OneToOneField(Appointment, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_date = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.appointment} - ${self.amount}"
