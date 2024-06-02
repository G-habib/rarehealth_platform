import os 
os.environ["CUDA_VISIBLE_DEVICES"] = "-1"
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from .models import *
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .decorators import patient_required, doctor_required
from django.contrib.auth.models import User
# Create your views here.

@login_required(login_url='login')
def home(request):
    return render(request,"index.html",{})

@login_required(login_url='login')
def diseases_view(request):
    return render(request, 'diseases.html')

@login_required(login_url='login')
def treatment_view(request):
    return render(request, 'treatment.html')

@login_required(login_url='login')
@patient_required
def patients_view(request):
    doc = Doctor.objects.all()
    d = {'doc': doc}
    return render(request, 'patients.html', d)

@login_required(login_url='login')
@doctor_required
def doctors_view(request):
    pat = Patient.objects.all()
    p = {'pat': pat}
    return render(request, 'doctors.html', p)

@login_required(login_url='login')
def location_view(request):
    return render(request, 'location.html')


@login_required(login_url='login')
def delete_appointment(request, aid):
    appointment = Appointement.objects.get(id = aid)
    appointment.delete()
    return redirect('view_appointment')

@login_required(login_url='login')
def delete_doc_appointment(request, aid):
    appointment = Appointement.objects.get(id = aid)
    appointment.delete()
    return redirect('view_doc_appointment')

@login_required(login_url='login')
def add_appointment(request):
    doctors = Doctor.objects.all()
    error = None

    if request.method == "POST":
        doctor_id = request.POST.get('doctor')
        date = request.POST.get('date')
        time = request.POST.get('time')
        
        try:
            doctor = Doctor.objects.get(id=doctor_id)
            patient = Patient.objects.get(email=request.user.email)  

            if date and time:
                Appointement.objects.create(
                    doctor=doctor,
                    patient=patient,
                    date=date,
                    time=time
                )
                messages.success(request, 'Appointment was made successfully. Check out the appointments page to see your appointments.')
                return redirect('view_appointment')
            else:
                error = "Please fill out all fields correctly."
        except Doctor.DoesNotExist:
            error = "Selected doctor does not exist."
        except Patient.DoesNotExist:
            error = "Patient not found."

    context = {'doctors': doctors, 'error': error}
    return render(request, 'add_appointment.html', context)

@login_required(login_url='login')
@patient_required
def appointment_view(request):
    try:
        patient = Patient.objects.get(email=request.user.email)
        appointments = Appointement.objects.filter(patient=patient)
    except Patient.DoesNotExist:
        appointments = []

    context = {'appointments': appointments}
    return render(request, 'view_appointment.html', context)

@login_required(login_url='login')
@doctor_required
def doc_appointment_view(request):
    try:
        doctor = Doctor.objects.get(email=request.user.email)
        appointments = Appointement.objects.filter(doctor=doctor)
    except Doctor.DoesNotExist:
        appointments = []

    context = {'appointments': appointments}
    return render(request, 'view_doc_appointment.html', context)

def get_full_name(user):
    try:
        if hasattr(user, 'doctor'):
            return f"{user.doctor.first_name} {user.doctor.last_name}"
        elif hasattr(user, 'patient'):
            return f"{user.patient.first_name} {user.patient.last_name}"
    except:
        return f"{user.username}"

@login_required(login_url='login')
@patient_required
def patients_msg_view(request):
    if request.method == 'POST':
        recipient_id = request.POST.get('recipient')
        content = request.POST.get('content')
        recipient = User.objects.get(id=recipient_id)
        Message.objects.create(sender=request.user, recipient=recipient, content=content)
        return redirect('patients_msg')
    
    doctors = Doctor.objects.all()
    sent_messages = Message.objects.filter(sender=request.user)
    received_messages = Message.objects.filter(recipient=request.user)
    sent_messages_data = [
        {
            'recipient_name': get_full_name(message.recipient),
            'content': message.content,
            'timestamp': message.timestamp
        }
        for message in sent_messages
    ]
    
    received_messages_data = [
        {
            'sender_name': get_full_name(message.sender),
            'content': message.content,
            'timestamp': message.timestamp
        }
        for message in received_messages
    ]
    
    context = {
        'doctors': doctors,
        'sent_messages': sent_messages_data,
        'received_messages': received_messages_data
    }
    return render(request, 'patients_msg.html', context)

@login_required(login_url='login')
@doctor_required
def doctors_msg_view(request):
    if request.method == 'POST':
        recipient_id = request.POST.get('recipient')
        content = request.POST.get('content')
        recipient = User.objects.get(id=recipient_id)
        Message.objects.create(sender=request.user, recipient=recipient, content=content)
        return redirect('doctors_msg')

    patients = Patient.objects.all()
    doctors = Doctor.objects.all()
    sent_messages = Message.objects.filter(sender=request.user)
    received_messages = Message.objects.filter(recipient=request.user)
    sent_messages_data = [
        {
            'recipient_name': get_full_name(message.recipient),
            'content': message.content,
            'timestamp': message.timestamp
        }
        for message in sent_messages
    ]
    
    received_messages_data = [
        {
            'sender_name': get_full_name(message.sender),
            'content': message.content,
            'timestamp': message.timestamp
        }
        for message in received_messages
    ]
    
    context = {
        'doctors': doctors,
        'patients': patients,
        'sent_messages': sent_messages_data,
        'received_messages': received_messages_data
    }
    return render(request, 'doctors_msg.html', context)
