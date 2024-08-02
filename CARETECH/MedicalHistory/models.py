from django.db import models
from account.models import Patient, HealthCareProvider


# Create your models here.

class Hospital(models.Model):
    name = models.CharField(max_length=100)
    address = models.TextField(max_length=1000)
    contact = models.TextField(max_length=1000)


class CurrentMedication(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    blood_pressure = models.CharField(max_length=100, null=True, blank=True)
    date = models.DateTimeField(auto_now_add=True)


class MedicalHistory(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    health_care_provider = models.ForeignKey(HealthCareProvider, on_delete=models.CASCADE)
    hospital = models.ForeignKey(Hospital, on_delete=models.CASCADE)
    prescription = models.ForeignKey(CurrentMedication, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)
