from django.urls import path
from .views import *

urlpatterns = [
    path('newbookRequest', newbookRequest, name='newbookRequest'),
    
]
    