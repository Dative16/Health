from django.shortcuts import render, redirect
from .forms import RegisterForm
from .models import Account, Patient
from django.contrib import messages, auth
from django.contrib.auth.decorators import login_required, permission_required


# Create your views here.


def home(request):
    return render(request, 'base/home.html')


def register(request):
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
            date_of_birth = form.cleaned_data['date_of_birth']
            password = form.cleaned_data['password']
            user = Account.objects.create_user(first_name=first_name, last_name=last_name, email=email,
                                               username=username, password=password)
            user.phone_number = phone_number
            user.gender = gender
            user.date_of_birth = date_of_birth
            user.age = user.date_of_joined.year - user.date_of_birth.year
            user.save()
            patient = Patient.objects.create(user=user)
            patient.save()
            messages.success(request, 'You are Successfully Registered!')
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
