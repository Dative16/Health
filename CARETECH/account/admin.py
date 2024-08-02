from django.contrib import admin
from .models import Account, Patient, HealthCareProvider

# Register your models here.

admin.site.register(Account)
admin.site.register(Patient)
admin.site.register(HealthCareProvider)
