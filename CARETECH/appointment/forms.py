from django import forms

from .models import Appointment


class AppointmentForm(forms.ModelForm):
    class Meta:
        model = Appointment
        fields = ['provider', 'description', 'hospitals']

    def __int__(self, *args, **kwargs):
        super(AppointmentForm, self).__init__(*args, **kwargs)
        self.fields['hospitals'].widgets.attrs['id'] = 'hospital'
        self.fields['hospitals'].widgets.attrs['name'] = 'hospital'

        self.fields['description'].widgets.attrs['placeholder'] = 'please Explain Why you are requesting the Appointment'
        self.fields['description'].widgets.attrs['id'] = 'description'
        self.fields['description'].widgets.attrs['name'] = 'description'

        self.fields['provider'].widgets.attrs['id'] = 'provider'
        self.fields['provider'].widgets.attrs['name'] = 'provider'
