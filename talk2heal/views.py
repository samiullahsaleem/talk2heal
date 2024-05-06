from django.contrib.auth import login, authenticate
from django.shortcuts import render, redirect, HttpResponse
from django.views.generic.edit import CreateView
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.views import LoginView, LogoutView
from .models import *
from .forms import *
from django.urls import reverse_lazy
from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from django.views.generic import View
import os
from django.http import HttpResponse
from django.conf import settings
from datetime import datetime, timedelta
from django.db.models import Sum
from django.db.models import Q

import cloudinary
from django.shortcuts import get_object_or_404

import requests
from django.contrib.auth import login, authenticate, logout
from django.shortcuts import render, redirect
from django.views.generic.edit import CreateView
from django.contrib.auth.forms import AuthenticationForm
from .models import *
from .forms import *
from django.urls import reverse_lazy
from django.views.generic import View
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from datetime import datetime, timedelta
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
import json
import stripe
from django.http import HttpResponseRedirect

def PsychologistLoginView(request):
    message = ''
    if request.method == 'POST':
        username = request.POST.get('username', '')
        password = request.POST.get('password', '')
        try:
            psychologist = Psychologist.objects.get(username=username, password=password)
            request.session['is_psychologist'] = True
            request.session['psychologist_id'] = psychologist.id
            request.session['is_patient'] = False
            return redirect('psychologist_appointments')
        except Psychologist.DoesNotExist:
            message = "Invalid username or password"
            pass
    return render(request, 'psychologist/login.html', {'message': message})

def PatientLoginView(request):
    message = ''
    if request.method == 'POST':
        username = request.POST.get('username', '')
        password = request.POST.get('password', '')
        try:
            patient = Patient.objects.get(username=username, password=password)
            request.session['is_patient'] = True
            request.session['patient_id'] = patient.id
            print(request.session.get('patient_id'))
            request.session['is_psychologist'] = False
            return redirect('patient_dashboard')
        except Patient.DoesNotExist:
            message = "Invalid username or password"
            pass
    return render(request, 'patient/login.html', {'message': message})
def PsychologistDashboardView(request):
    if request.session.get('is_psychologist'):
        return render(request, 'psychologist/dashboard.html')
    else:
        return redirect('psychologist_login')

def PatientDashboardView(request):
    if request.session.get('is_patient'):
        return render(request, 'patient/dashboard.html')
    else:
        return redirect('patient_login')


def PsychologistSignUpView(request):
    if request.method == 'POST':
        # Extract data from the POST request
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')  # Use password1 for password
        name = request.POST.get('name')
        address = request.POST.get('address')
        degree = request.POST.get('degree')
        years_of_experience = request.POST.get('years_of_experience')
        city = request.POST.get('city')
        rate = request.POST.get('rate')

        # Save the Psychologist instance
        psychologist = Psychologist.objects.create(
            username=username,
            email=email,
            password=password,
            name=name,
            address=address,
            degree=degree,
            years_of_experience=years_of_experience,
            city=city,
            rate=rate,
            account_verified_status='pending'  # Set any default values you need
        )

        # Process and save the profile picture on Cloudinary
        profile_picture = request.FILES.get('profile_picture')
        if profile_picture:
            result = cloudinary.uploader.upload(profile_picture)
            psychologist.profile_picture = result['url']
            psychologist.save()

        # Redirect to the login page after successful signup
        return redirect('psychologist_login')

    return render(request, 'psychologist/signup.html')

def PatientSignUpView(request):
    if request.method == 'POST':
        # Extract data from the POST request
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')  # Use password1 for password
        name = request.POST.get('name')
        address = request.POST.get('address')
        contact_number = request.POST.get('contact_number')
        city = request.POST.get('city')

        # Save the Patient instance
        patient = Patient.objects.create(
            username=username,
            email=email,
            password=password,
            name=name,
            address=address,
            contact_number=contact_number,
            city=city

        )

        # Process and save the profile picture on Cloudinary
        profile_picture = request.FILES.get('profile_picture')
        if profile_picture:
            result = cloudinary.uploader.upload(profile_picture)
            patient.profile_picture = result['url']
            patient.save()

        # Redirect to the login page after successful signup
        return redirect('patient_login')

    return render(request, 'patient/signup.html')

def PsychologistLogoutView(request):
    request.session.flush()

    
    return redirect('psychologist_login')

def PatientLogoutView(request):
    request.session.flush()
    return redirect('patient_login')


class PsychologistProfileView(View):
    template_name = 'psychologist/profile.html'

    def get(self, request, *args, **kwargs):
        if request.session.get('is_psychologist'):
            psychologist = Psychologist.objects.get(id=request.session.get('psychologist_id'))
            print(psychologist.profile_picture.url)
            return render(request, self.template_name, {'psychologist': psychologist})
        else:
            return redirect('psychologist_login')
class PatientProfileView(View):
    template_name = 'patient/profile.html'

    def get(self, request, *args, **kwargs):
        if request.session.get('is_patient'):
            patient = Patient.objects.get(id=request.session.get('patient_id'))
            print(patient.profile_picture.url)
            return render(request, self.template_name, {'patient': patient})
        else:
            return redirect('patient_login')
        

def update_psychologist_profile(request, psychologist_id):
    if request.session.get('is_psychologist'):
        psychologist = get_object_or_404(Psychologist, id=psychologist_id)

        if request.method == 'POST':
            # Update profile fields
            psychologist.name = request.POST.get('name')
            psychologist.address = request.POST.get('address')
            psychologist.degree = request.POST.get('degree')
            psychologist.years_of_experience = request.POST.get('years_of_experience')
            psychologist.city = request.POST.get('city')
            psychologist.rate = request.POST.get('rate')
        

            # Update profile picture if provided
            profile_picture = request.FILES.get('profile_picture')
            if profile_picture:
                psychologist.profile_picture = profile_picture

            # Save the changes
            psychologist.save()

            return redirect('psychologist_profile')

        return render(request, 'psychologist/update_profile.html', {'psychologist': psychologist})
    else:
        return redirect('psychologist_login')
def update_patient_profile(request, patient_id):
    patient = get_object_or_404(Patient, id=patient_id)

    if request.method == 'POST':
        # Update profile fields
        patient.name = request.POST.get('name')
        patient.address = request.POST.get('address')
        patient.contact_number = request.POST.get('contact_number')
        patient.city = request.POST.get('city')
        
    

        # Update profile picture if provided
        profile_picture = request.FILES.get('profile_picture')
        if profile_picture:
            patient.profile_picture = profile_picture

        # Save the changes
        patient.save()

        return redirect('patient_profile')

    return render(request, 'patient/update_profile.html', {'patient': patient})


def delete_psychologist_profile(request, psychologist_id):
    psychologist = get_object_or_404(Psychologist, id=psychologist_id)

    if request.method == 'POST':
        # Delete the psychologist profile
        psychologist.delete()
        return redirect('psychologist_signup')  # Redirect to the psychologist dashboard or any other page

    return render(request, 'psychologist/delete_profile.html', {'psychologist': psychologist})


def delete_patient_profile(request, patient_id):
    patient = get_object_or_404(Patient, id=patient_id)

    if request.method == 'POST':
        # Delete the patient profile
        patient.delete()
        return redirect('patient_signup')  # Redirect to the patient dashboard or any other page

    return render(request, 'patient/delete_profile.html', {'patient': patient})

# def zoom_oauth_redirect(request):
#     # Redirect user to Zoom OAuth authorization URL
#     zoom_authorization_url = f'https://zoom.us/oauth/authorize?client_id=GBT_KwULROyywhvM7FsNg&response_type=code&redirect_uri=http%3A%2F%2F127.0.0.1%3A8000%2Ftalk2heal%2Fzoom%2Foauth%2Fcallback%2F'
#     return redirect(zoom_authorization_url)

# def zoom_oauth_callback(request):
#     # Handle OAuth callback from Zoom
#     code = request.GET.get('code')
    
#     # Exchange authorization code for an access token
#     token_url = 'https://zoom.us/oauth/token'
#     token_data = {
#         'grant_type': 'authorization_code',
#         'code': code,
#         'redirect_uri': settings.ZOOM_REDIRECT_URI,
#         'client_id': settings.ZOOM_CLIENT_ID,
#         'client_secret': settings.ZOOM_CLIENT_SECRET,
#     }

#     response = requests.post(token_url, data=token_data)
#     access_token = response.json().get('access_token')

#     # Store the access token securely in your database or session
#     request.session['zoom_access_token'] = access_token

#     return render(request, 'zoom_oauth_success.html')

# def create_zoom_meeting(request):
    # Get the stored access token
    access_token = request.session.get('zoom_access_token')
    
    if not access_token:
        return HttpResponse('Zoom access token not found. Please authenticate via OAuth.')

    # Set up meeting details (you can customize this based on your needs)
    meeting_data = {
        'topic': 'My Scheduled Meeting',
        'type': 2,  # Scheduled meeting
        'start_time': (datetime.now() + timedelta(minutes=10)).strftime('%Y-%m-%dT%H:%M:%S'),
        'duration': 30,  # Duration in minutes
    }

    # Make a Zoom API request to schedule a meeting
    create_meeting_url = 'https://api.zoom.us/v2/users/me/meetings'
    headers = {'Authorization': f'Bearer {access_token}', 'Content-Type': 'application/json'}
    
    response = requests.post(create_meeting_url, json=meeting_data, headers=headers)

    if response.status_code == 201:
        meeting_info = response.json()
        meeting_id = meeting_info.get('id')
        join_url = meeting_info.get('join_url')
        
        # You can save the meeting_id in your database for future reference

        return render(request, 'meeting_created.html', {'meeting_id': meeting_id, 'join_url': join_url})

    return HttpResponse(f'Failed to create Zoom meeting. Error: {response.text}')



# SCOPES = ['https://www.googleapis.com/auth/calendar']

# def authenticate_google_calendar():
    # secret_file_path = os.path.join(os.path.dirname(__file__), 'secret.json')
    # flow = InstalledAppFlow.from_client_secrets_file(
    #     secret_file_path, SCOPES)
#     creds = flow.run_local_server(port=0)
#     return creds
# def create_google_meet_meeting():
#     creds = authenticate_google_calendar()
#     service = build('calendar', 'v3', credentials=creds)

#     # Set up meeting details
#     meeting = {
#         'summary': 'My Google Meet Meeting',
#         'description': 'Meeting Description',
#         'start': {
#             'dateTime': (datetime.now() + timedelta(minutes=10)).isoformat(),
#             'timeZone': 'UTC',
#         },
#         'end': {
#             'dateTime': (datetime.now() + timedelta(minutes=30)).isoformat(),
#             'timeZone': 'UTC',
#         },
#         'conferenceData': {
#             'createRequest': {
#                 'requestId': 'random-string-id',
#             },
#         },
#     }

#     # Create the event and return meeting link
#     event = service.events().insert(calendarId='primary', body=meeting, conferenceDataVersion=1).execute()
#     meeting_link = event['conferenceData']['entryPoints'][0]['uri']

#     print(meeting_link)
# def create_google_meeting(request):
#     # Check for existing Google Calendar credentials in the session
#     creds_json = request.session.get('google_calendar_credentials')

#     if not creds_json:
#         # Redirect to OAuth authorization if credentials are not found
#         return redirect('google_oauth_authorize')

#     # Load stored credentials
#     creds = Credentials.from_authorized_user_info(json.loads(creds_json), scopes=['https://www.googleapis.com/auth/calendar'])

#     # Create a Google Calendar API service
#     service = build('calendar', 'v3', credentials=creds)
#     print("Yes")

#     # Set up meeting details (you can customize this based on your needs)
#     meeting_data = {
#         'summary': 'My Scheduled Meeting',
#         'description': 'This is a Google Meet meeting scheduled through Django.',
#         'start': {
#             'dateTime': (datetime.now() + timedelta(minutes=10)).isoformat(),
#             'timeZone': 'UTC',
#         },
#         'end': {
#             'dateTime': (datetime.now() + timedelta(minutes=40)).isoformat(),
#             'timeZone': 'UTC',
#         },
#         'conferenceData': {
#             'createRequest': {
#                 'requestId': 'test-conference-request',
#             },
#         },
#     }
def create_google_meeting(request, appointment_date):
    print("T")
    # Check for existing Google Calendar credentials in the session
    creds_json = request.session.get('google_calendar_credentials')

    if not creds_json:
        print("Coming here too")
        # Redirect to OAuth authorization if credentials are not found
        return redirect('google_oauth_authorize')

    # Load stored credentials
    creds = Credentials.from_authorized_user_info(json.loads(creds_json), scopes=['https://www.googleapis.com/auth/calendar'])
    print("Yes working")
    # Create a Google Calendar API service
    service = build('calendar', 'v3', credentials=creds)
    
    
    appointment_datetime = appointment_date
    meeting_data = {
        'summary': 'My Scheduled Meeting',
        'description': 'This is a Google Meet meeting scheduled through Django.',
        'start': {
            'dateTime': appointment_datetime.isoformat(),
            'timeZone': 'UTC',
            
        },
        'end': {
            'dateTime': (appointment_datetime + timedelta(minutes=30)).isoformat(),
            'timeZone': 'UTC',
        },

        'conferenceData': {
            'createRequest': {
                'requestId': 'test-conference-request',
            },
        },
    }
   
    # Make a Google Calendar API request to schedule a meeting

    meeting_info = service.events().insert(
        calendarId='primary',
        body=meeting_data,
        conferenceDataVersion=1,
    ).execute()

    meeting_url = meeting_info.get('hangoutLink')
    print(meeting_url)

    return meeting_url        
def google_oauth_authorize():
    # Set up Google Calendar API OAuth flow
    print("Coming here")
    SCOPES = ['https://www.googleapis.com/auth/calendar']
    secret_file_path = os.path.join(os.path.dirname(__file__), 'secret.json')
    flow = InstalledAppFlow.from_client_secrets_file(
        secret_file_path, SCOPES,
        redirect_uri='https://127.0.0.1:8000/talk2heal/create_google_meeting/oauth2callback/')

    authorization_url, _ = flow.authorization_url(prompt='consent')

    return redirect(authorization_url)

def google_oauth_callback(request):
    # Handle OAuth callback from Google
    SCOPES = ['https://www.googleapis.com/auth/calendar']
    secret_file_path = os.path.join(os.path.dirname(__file__), 'secret.json')
    flow = InstalledAppFlow.from_client_secrets_file(
        secret_file_path, SCOPES,
        redirect_uri='https://127.0.0.1:8000/talk2heal/create_google_meeting/oauth2callback/')

    authorization_response = request.build_absolute_uri()
    flow.fetch_token(authorization_response=authorization_response)

    creds = flow.credentials
    request.session['google_calendar_credentials'] = creds.to_json()

    return redirect('create_google_meeting')


def psychologists_list(request):
    psychologists = Psychologist.objects.all()

    # Get the logged-in patient's city
    patient = Patient.objects.get(id=request.session.get('patient_id'))
    patient_city = patient.city
    
    # Get recommended psychologists based on the patient's city
    recommended_psychologists = psychologists.filter(city=patient_city)
    is_patient = False
    if request.session.get('is_patient'):
        is_patient = True
    context = {
        'psychologists': psychologists,
        'recommended_psychologists': recommended_psychologists,
        'is_patient': is_patient ,
    }
    print(context['is_patient'])
    return render(request, 'psychologist/psychologists_list.html', context)

def book_appointment(request, psychologist_id):
    if not request.session.get('is_patient'):
        return redirect('patient_login')

    psychologist = get_object_or_404(Psychologist, id=psychologist_id)

    if request.method == 'POST':
        # Process appointment booking logic here
        # Retrieve patient-selected details such as location and appointment type
        location = request.POST.get('location')  # Assuming you have a form field named 'location'
        appointment_date = request.POST.get('appointment_date')
        # appointment_time = request.POST.get('appointment_time')
        patient = Patient.objects.get(id=request.session.get('patient_id'))

        # Save the appointment (create a new Appointment instance)
        appointment = Appointment.objects.create(
            patient=patient,  # Assuming you have patient authentication
            psychologist=psychologist,
            appointment_date=appointment_date,
            location=location,
        )

        # Redirect to the payment page (Stripe integration)
        return redirect('stripe_payment', appointment_id=appointment.id)

    return render(request, 'psychologist/book_appointment.html', {'psychologist': psychologist})


def stripe_payment(request, appointment_id):
    appointment = get_object_or_404(Appointment, id=appointment_id)

    if request.method == 'POST':
        # Process Stripe payment logic here
        stripe.api_key = 'sk_test_51FSSm3DYZLUHoAttx0qDjAPgSzDqFpl49yYC6uLHt4ye9w6PK7NPlEocI4cbNOslb3WA5R7PcrQmEnz5mowmyjnv00n4qpXqyM'  # Replace with your actual Stripe secret key

        # Charge the patient for the appointment amount
        charge = stripe.Charge.create(
            amount=int(appointment.psychologist.rate * 100),  # Convert rate to cents
            currency='usd',
            description=f'Appointment with {appointment.psychologist.name}',
            source=request.POST['stripeToken'],  # This assumes you have a Stripe.js token
        )
        if(appointment.location=="online"):
            print("Yes coming here")
            meeting_link = create_google_meeting(request, appointment.appointment_date)
            appointment.chat_link = "https://meet.google.com/eyr-vsjr-grf"
        else:
            appointment.chat_link = appointment.psychologist.address    
        appointment.is_paid = True
        appointment.payment_date = timezone.now()
        appointment.save()

        # Redirect to a success page or display a success message
        return render(request, 'payment_success.html', {'appointment': appointment})

    return render(request, 'stripe_payment.html', {'appointment': appointment})

def patient_appointments(request):
    if not request.session.get('is_patient'):
        return redirect('patient_login')

    patient_id = request.session.get('patient_id')
    appointments = Appointment.objects.filter(patient__id=patient_id).order_by('appointment_date')
    for a in appointments:
        print(a.chat_link)
    
    print(datetime.now().minute)
    print(appointments[0].appointment_date.minute)

    return render(request, 'patient/appointment.html', {'appointments': appointments, 'today': datetime.now().minute,'todaydate':datetime.now()})


def psychologist_appointments(request):
    if not request.session.get('is_psychologist'):
        return redirect('psychologist_login')

    psychologist_id = request.session.get('psychologist_id')
    appointments = Appointment.objects.filter(psychologist__id=psychologist_id)

    return render(request, 'psychologist/appointment.html', {'appointments': appointments, 'today': datetime.now()})

def psychologist_earnings(request):
    if not request.session.get('is_psychologist'):
        return redirect('psychologist_login')

    psychologist_id = request.session.get('psychologist_id')
    earnings = Appointment.objects.filter(
        psychologist__id=psychologist_id,
        is_paid=True
    ).aggregate(Sum('psychologist__rate'))['psychologist__rate__sum'] or 0

    return render(request, 'psychologist/earnings.html', {'earnings': earnings})

def patient_spendings(request):
    if not request.session.get('is_patient'):
        return redirect('patient_login')

    patient_id = request.session.get('patient_id')
    spendings = Appointment.objects.filter(
        patient__id=patient_id,
        is_paid=True
    ).aggregate(Sum('psychologist__rate'))['psychologist__rate__sum'] or 0

    return render(request, 'patient/spendings.html', {'spendings': spendings})


# views.py



def search_psychologists(request):
    query = request.GET.get('q')

    if query:
        psychologists = Psychologist.objects.filter(
            Q(name__icontains=query) |  # Search by psychologist name (case-insensitive)
            Q(degree__icontains=query)  | # Search by psychologist degree (case-insensitive)
            Q(city__icontains=query ) # Search by psychologist city (case-insensitive)


        )
    else:
        psychologists = Psychologist.objects.all()
    patient = Patient.objects.get(id=request.session.get('patient_id'))
    patient_city = patient.city
    
    recommended_psychologists = psychologists.filter(city=patient_city)

    return render(request, 'psychologist/psychologists_list.html', {'psychologists': psychologists, 'recommended_psychologists': recommended_psychologists})

def chat(request):
    if request.session["is_patient"]:
        psychologists = Psychologist.objects.all()
        patient = Patient.objects.get(id=request.session.get('patient_id'))
        patient_city = patient.city
    
        recommended_psychologists = psychologists.filter(city=patient_city)
        return render(request, 'chatbot/chat.html', {'psychologists': psychologists, 'recommended_psychologists': recommended_psychologists})
    else:
        return redirect('patient_login')

def errorpage(request,exception):
    return render(request, '404.html',  status=404)