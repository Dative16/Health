from django.shortcuts import render, redirect, get_object_or_404

from MedicalHistory.models import MedicalHistory
from appointment.models import Appointment
from .forms import RegisterForm
from .models import Account, Patient
from django.contrib import messages, auth
from django.contrib.auth.decorators import login_required

# Create your views here.
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import EmailMessage


def home(request):
    profile = Account.objects.filter(username=request.user.username)
    patient = get_object_or_404(Patient, user=request.user)
    medical_history = MedicalHistory.objects.filter(patient=patient)
    appointments = Appointment.objects.filter(patient=patient)
    appointment_count = appointments.count()

    context = {
        'profile': profile,
        'patient': patient,
        'medical_history': medical_history,
        'appointments': appointments,
        'appointment_count': appointment_count,
    }
    return render(request, 'base/home.html', context)


def register_user(request):
    form = RegisterForm()
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            email = form.cleaned_data['email']
            username = form.cleaned_data['username']
            phone_number = form.cleaned_data['phone_number']
            gender = form.cleaned_data['gender']
            date_of_birth = request.POST['date_of_birth']
            password = form.cleaned_data['password']
            user = Account.objects.create_user(first_name=first_name, last_name=last_name, email=email,
                                               username=username, password=password)
            user.phone_number = phone_number
            user.gender = gender
            user.date_of_birth = date_of_birth
            user.age = user.date_of_joined.year - int(date_of_birth.split('-')[0])
            user.save()
            patient = Patient.objects.create(user=user)
            patient.save()
            messages.success(request, 'You are Successfully Registered!')
            # user activation
            current_site = get_current_site(request)
            mail_subject = 'Please activate your account'
            message = render_to_string('account_verification_email.html', {
                'user': user,
                'domain': current_site,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': default_token_generator.make_token(user),
            })
            to_email = email
            send_email = EmailMessage(mail_subject, message, to=[to_email])
            send_email.send()

            return redirect('login')
    context = {
        'form': form
    }
    return render(request, 'register.html', context=context)


def login(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        try:

            user = auth.authenticate(email=email, password=password)
            if user is not None:
                auth.login(request, user)
                messages.success(request, "Login Successfully!")
                return redirect('/')
            else:
                messages.error(request, 'Invalid credential')
                return redirect('login')
        except Exception as e:
            messages.error(request, e)
            return redirect('login')
    return render(request, 'login.html')


@login_required(login_url='login')
def logout(request):
    auth.logout(request)
    messages.success(request, "You are Logged Out")
    return redirect('login')


@login_required(login_url='login')
def view_profile(request):
    profile = Account.objects.filter(username=request.user.username)
    patient = get_object_or_404(Patient, user=request.user)
    medical_history = MedicalHistory.objects.filter(patient=patient)
    appointments = Appointment.objects.filter(patient=patient)
    appointment_count = appointments.count()

    context = {
        'profile': profile,
        'patient': patient,
        'medical_history': medical_history,
        'appointments': appointments,
        'appointment_count': appointment_count,
    }
    return render(request, 'profile.html', context)


def activate(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = Account._default_manager.get(pk=uid)
    except(TypeError, ValueError, OverflowError, Account.DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        user.is_active = True
        user.save()
        messages.success(request, 'Congratulations! Your account is activated.')
        return redirect('login')
    else:
        messages.error(request, 'Invalid activation link')
        return redirect('register')


def forgotPassword(request):
    if request.method == 'POST':
        email = request.POST['email']
        if Account.objects.filter(email=email).exists():
            user = Account.objects.get(email__exact=email)

            # Reset password email
            current_site = get_current_site(request)
            mail_subject = 'Reset Your Password'
            message = render_to_string('reset_password_email.html', {
                'user': user,
                'domain': current_site,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': default_token_generator.make_token(user),
            })
            to_email = email
            send_email = EmailMessage(mail_subject, message, to=[to_email])
            send_email.send()

            messages.success(request, 'Password reset email has been sent to your email address.')
            return redirect('login')
        else:
            messages.error(request, 'Account of that Email does not exist!')
            return redirect('forgotPassword')
    return render(request, 'forgotPassword.html')


def resetpassword_validate(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = Account._default_manager.get(pk=uid)
    except(TypeError, ValueError, OverflowError, Account.DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        request.session['uid'] = uid
        messages.success(request, 'Please reset your password')
        return redirect('resetPassword')
    else:
        messages.error(request, 'This link has been expired!')
        return redirect('login')


def resetPassword(request):
    if request.method == 'POST':
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']

        if password == confirm_password:
            uid = request.session.get('uid')
            user = Account.objects.get(pk=uid)
            user.set_password(password)
            user.save()
            messages.success(request, 'Password reset successful')
            return redirect('login')
        else:
            messages.error(request, 'Password do not match!')
            return redirect('resetPassword')
    else:
        return render(request, 'resetPassword.html')


@login_required(login_url='login')
def change_password(request):
    if request.method == 'POST':
        current_password = request.POST['current_password']
        new_password = request.POST['new_password']
        confirm_password = request.POST['confirm_password']

        user = Account.objects.get(username__exact=request.user.username)

        if new_password == confirm_password:
            success = user.check_password(current_password)
            if success:
                user.set_password(new_password)
                user.save()
                # auth.logout(request)
                messages.success(request, 'Password updated successfully.')
                return redirect('change_password')
            else:
                messages.error(request, 'Please enter valid current password')
                return redirect('change_password')
        else:
            messages.error(request, 'Password does not match!')
            return redirect('change_password')
    return render(request, 'change_password.html')
