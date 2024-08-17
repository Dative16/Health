from django.urls import path
from .views import create_appointment

urlpatterns = [
    path('create_appointment/', create_appointment, name='create_appointment'),
]
