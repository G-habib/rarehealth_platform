from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.contrib.auth.models import User
from base.models import Patient, Doctor

class PatientRegisterForm(UserCreationForm):
    email = forms.EmailField()
    first_name = forms.CharField(max_length=50)
    last_name = forms.CharField(max_length=50)
    gender = forms.ChoiceField(choices=Patient.GENDER)
    phone = forms.CharField(max_length=20)
    country = forms.CharField(max_length=50)
    city = forms.CharField(max_length=50)
    address = forms.CharField(max_length=200)

    class Meta:
        model = User
        fields = ["username", "email", "password1", "password2"]

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
            Patient.objects.create(
                user=user,
                first_name=self.cleaned_data['first_name'],
                last_name=self.cleaned_data['last_name'],
                gender=self.cleaned_data['gender'],
                phone=self.cleaned_data['phone'],
                email=self.cleaned_data['email'],
                country=self.cleaned_data['country'],
                city=self.cleaned_data['city'],
                address=self.cleaned_data['address']
            )
        return user

class DoctorRegisterForm(UserCreationForm):
    email = forms.EmailField()
    first_name = forms.CharField(max_length=50)
    last_name = forms.CharField(max_length=50)
    specialty = forms.ChoiceField(choices=Doctor.SPECIALTY)
    approval_number = forms.CharField(max_length=50)
    phone = forms.CharField(max_length=20)
    country = forms.CharField(max_length=50)
    city = forms.CharField(max_length=50)
    work_address = forms.CharField(max_length=200)

    class Meta:
        model = User
        fields = ["username", "email", "password1", "password2"]

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
            Doctor.objects.create(
                user=user,
                first_name=self.cleaned_data['first_name'],
                last_name=self.cleaned_data['last_name'],
                specialty=self.cleaned_data['specialty'],
                approval_number=self.cleaned_data['approval_number'],
                phone=self.cleaned_data['phone'],
                email=self.cleaned_data['email'],
                country=self.cleaned_data['country'],
                city=self.cleaned_data['city'],
                work_address=self.cleaned_data['work_address'],
                status='pending'
            )
        return user
