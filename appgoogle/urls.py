from django.contrib import admin
from django.urls import path,include

urlpatterns = [
    #contas-login
    path('', include('allauth.urls')),
]