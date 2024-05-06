from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import Psychologist, Patient

class PsychologistSignUpForm(forms.ModelForm):
    class Meta:
        model = Psychologist
        fields = ["username", "email", "password", "name",  "years_of_experience", "degree", "contact_number", "address"]

class PatientSignUpForm(forms.ModelForm ):
    class Meta:
        model = Patient
        fields = ["username", "email", "password", "name"]

class PsychologistLoginForm(forms.Form):
    username = forms.CharField(label='Username', widget=forms.TextInput(attrs={'class': 'fadeIn second', 'placeholder': 'Username'}))
    password = forms.CharField(label='Password', widget=forms.PasswordInput(attrs={'class': 'fadeIn second', 'placeholder': 'Password'}))

class PatientLoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)
