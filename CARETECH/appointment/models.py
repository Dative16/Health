from django.db import models
from account.models import Patient, HealthCareProvider
from MedicalHistory.models import Hospital

# Create your models here.

STATUS = [
    ('requested', 'requested'),
    ('scheduled', 'scheduled'),
    ('completed', 'completed'),
    ('cancelled', 'cancelled'),
    ('approved', 'approved'),
]


class Appointment(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    provider = models.ForeignKey(HealthCareProvider, on_delete=models.CASCADE)
    hospitals = models.ForeignKey(Hospital, on_delete=models.CASCADE)
    appointment_date = models.DateTimeField(auto_now=True)
    description = models.CharField(max_length=500, null=True, blank=True)
    status = models.CharField(max_length=100, choices=STATUS)
    is_active = models.BooleanField(default=False)

    class Meta:
        verbose_name = 'Appointment'
        verbose_name_plural = 'Appointments'

    def __str__(self):
        return f"{self.patient.user.first_name} {self.patient.user.last_name}"
