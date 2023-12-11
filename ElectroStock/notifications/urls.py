from django.urls import path
from .views import *
from rest_framework import routers
from rest_framework.authtoken.views import obtain_auth_token



urlpatterns = [
    path("test/", create_test_notification, name="test_notification"),
    
] 
