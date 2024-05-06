# backends.py
from django.contrib.auth.backends import ModelBackend
from .models import Psychologist, Patient

class PsychologistBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        try:
            user = Psychologist.objects.get(username=username)
        except Psychologist.DoesNotExist:
            return None

        if user.check_password(password):
            return user

class PatientBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        try:
            user = Patient.objects.get(username=username)
        except Patient.DoesNotExist:
            return None

        if user.check_password(password):
            return user
