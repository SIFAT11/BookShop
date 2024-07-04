from django.urls import path
from .views import *

urlpatterns = [
     path('reg/',register_profile, name='Registreation'), 
     path('login/',login_view, name='Login'),
     path('logout/',logout_view, name='logout'),
]

