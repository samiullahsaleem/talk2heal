from django.contrib import admin
from django.urls import path
from .views import *
from django.conf import settings
from django.conf.urls.static import static
from django.urls import re_path
from django.views.defaults import page_not_found


urlpatterns = [
    path('', PsychologistLoginView, name='psychologists_list'),
    path('psychologist/login/', PsychologistLoginView, name='psychologist_login'),
    path('psychologist/signup/', PsychologistSignUpView, name='psychologist_signup'),
    path('psychologist/dashboard/', PsychologistDashboardView, name='psychologist_dashboard'),
    path('patient/login/', PatientLoginView, name='patient_login'),
    path('patient/signup/', PatientSignUpView, name='patient_signup'),
    path('patient/dashboard/', psychologists_list, name='patient_dashboard'  ),
    path('psychologist/logout/', PsychologistLogoutView, name='psychologist_logout'),
    path('patient/logout/', PatientLogoutView, name='patient_logout'),
    path('psychologist/profile/', PsychologistProfileView.as_view(), name='psychologist_profile'),
    path('psychologist/<int:psychologist_id>/update/', update_psychologist_profile, name='update_psychologist_profile'),
    path('psychologist/<int:psychologist_id>/delete/', delete_psychologist_profile, name='delete_psychologist_profile'),
    path('patient/profile/', PatientProfileView.as_view(), name='patient_profile'),
    path('patient/<int:patient_id>/update/', update_patient_profile, name='update_patient_profile'),
    path('patient/<int:patient_id>/delete/', delete_patient_profile, name='delete_patient_profile'),
    path('create_google_meeting/', create_google_meeting, name='create_google_meeting'),
    path('google_oauth_authorize/', google_oauth_authorize, name='google_oauth_authorize'),
    path('create_google_meeting/oauth2callback/', google_oauth_callback, name='google_oauth_callback'),
    path('psychologists/', psychologists_list, name='psychologists_list'),
    path('book_appointment/<int:psychologist_id>/', book_appointment, name='book_appointment'),
    path('stripe_payment/<int:appointment_id>/', stripe_payment, name='stripe_payment'),
    path('psychologist/appointments/', psychologist_appointments, name='psychologist_appointments'),
    path('patient/appointments/', patient_appointments, name='patient_appointments'),
    path('psychologist/earnings/', psychologist_earnings, name='psychologist_earnings'),
    path('patient/spendings/', patient_spendings, name='patient_spendings'),
    path('search-psychologists/', search_psychologists, name='search_psychologists'),
    path('chat/', chat, name='chat'),
]

# Additional URLs like Psychologist and Patient specific pages can be added here


urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += [
    re_path(r'^.*/$', errorpage, {'exception': Exception('Page not Found')}),
]