from django.shortcuts import render, redirect
from .forms import PatientRegisterForm, DoctorRegisterForm
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import user_passes_test
import logging
from base.models import Doctor
#
def register(request):
    if request.user.is_authenticated:
        return redirect("/")
    else:
        if request.method == "POST":
            user_type = request.POST.get('user_type')
            if user_type == 'patient':
                patient_form = PatientRegisterForm(request.POST)
                if patient_form.is_valid():
                    patient_form.save()
                    messages.success(request, "Registration successful.")
                    return redirect("/")
                else:
                    messages.error(request, "Registration failed. Please ensure the form is valid.")
        else:
            patient_form = PatientRegisterForm()
        context = {
            'patient_form': patient_form,
        }
        return render(request, "register/register.html", context)

def doctor_request(request):
    if request.user.is_authenticated:
        return redirect("/")
    else:
        if request.method == "POST":
            doctor_form = DoctorRegisterForm(request.POST)
            if doctor_form.is_valid():
                doctor = doctor_form.save()
                doctor.status = 'pending'
                messages.success(request, "Registration request submitted. Please wait for approval.")
                return redirect("registration_status")
            else:
                messages.error(request, "Registration failed. Please ensure the form is valid.")
        else:
            doctor_form = DoctorRegisterForm()
        context = {
            'doctor_form': doctor_form,
        }
        return render(request, "register/doctor_request.html", context)

def registration_status(request):
    if not request.user.is_authenticated or not hasattr(request.user, 'doctor'):
        messages.error(request, "You are not authorized to view this page.")
        return redirect('login')
    
    doctor = request.user.doctor
    context = {
        'status': doctor.status,
    }
    return render(request, "register/registration_status.html", context)

def loginpage(request):
    if request.user.is_authenticated:
        if hasattr(request.user, 'doctor') and request.user.doctor.status == 'pending':
            return redirect('registration_status')
        return redirect("/")
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            if hasattr(user, 'doctor') and user.doctor.status == 'pending':
                login(request, user)
                return redirect('registration_status')
            login(request, user)
            return redirect('/')
        messages.info(request, 'Username OR password is incorrect')
    return render(request, 'registration/login.html')

def logoutuser(request):
    logout(request)
    return redirect('login')

logger = logging.getLogger(__name__)
def is_approved_doctor(user):
    if hasattr(user, 'doctor'):
        logger.info(f"Doctor status for user {user.username}: {user.doctor.status}")
        return user.doctor.status == 'approved'
    else:
        logger.info(f"User {user.username} is not a doctor")
        return True

@login_required(login_url='login')
@user_passes_test(is_approved_doctor, login_url='registration_status', redirect_field_name=None)
def home(request):
    return render(request, "index.html", {})
