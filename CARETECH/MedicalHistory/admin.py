from django.contrib import admin
from .models import MedicalHistory, CurrentMedication, Hospital

# Register your models here.
admin.site.register((CurrentMedication, Hospital, MedicalHistory))
# admin.site.register(MedicalHistory)
