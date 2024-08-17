from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect

from account.models import Patient
from django.template.loader import render_to_string
from django.core.mail import EmailMessage
from django.contrib import messages
from appointment.forms import AppointmentForm
from appointment.models import Appointment


@login_required(login_url="/accounts/login/")
def create_appointment(request):
    if request.method == 'POST':
        form = AppointmentForm(request.POST, request.FILES)
        if form.is_valid():
            description = form.cleaned_data['description']
            hospital = form.cleaned_data['hospitals']
            provider = form.cleaned_data['provider']
            patient = Patient.objects.filter(user=request.user)
            appointment = Appointment.objects.create(description=description, hospitals=hospital, provider=provider,
                                                     patient=patient[0])
            appointment.status = 'requested'
            appointment.save()

            messages.success(request, 'Your appointment has been created!')

            # Send order recieved email to customer
            mail_subject = 'Appointment Created! '
            message = render_to_string('appointment/appointment_created_email.html', {
                'user': request.user,
                'appointment': appointment,
            })
            to_email = request.user.email
            send_email = EmailMessage(mail_subject, message, to=[to_email])
            send_email.send()
            messages.success(request, 'Check Your Email We sent and Email For Your Appointment!')
            return redirect('home')
    form = AppointmentForm()
    context = {'form': form}
    return render(request, 'appointment/create_appointments.html', context)
