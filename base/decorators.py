from django.shortcuts import redirect
from django.contrib.auth.models import User
from .models import Patient, Doctor

def patient_required(view_func):
    def _wrapped_view_func(request, *args, **kwargs):
        if request.user.is_authenticated and (hasattr(request.user, 'patient') or request.user.is_superuser):
            return view_func(request, *args, **kwargs)
        else:
            return redirect('home')
    return _wrapped_view_func

def doctor_required(view_func):
    def _wrapped_view_func(request, *args, **kwargs):
        if request.user.is_authenticated and (hasattr(request.user, 'doctor') or request.user.is_superuser):
            return view_func(request, *args, **kwargs)
        else:
            return redirect('home')
    return _wrapped_view_func
