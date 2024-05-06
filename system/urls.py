from django.contrib import admin
from django.urls import path, include
from django.urls import re_path
from django.views.defaults import page_not_found
from talk2heal.views import errorpage

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('talk2heal.urls')),
    
]
urlpatterns += [
    re_path(r'^.*/$', errorpage, {'exception': Exception('Page not Found')}),
]
