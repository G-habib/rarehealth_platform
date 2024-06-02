from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Patient(models.Model):
    GENDER = (
        ('Male', 'Male'),
        ('Female','Female'),
    )
    #user = models.OneToOneField(User, on_delete=models.CASCADE)
    user = models.OneToOneField(User, null=True, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=50, null=True)
    last_name = models.CharField(max_length=50, null=True)
    gender = models.CharField(max_length=200, null=True, choices=GENDER)
    phone = models.CharField(max_length=20, null=True)
    email = models.CharField(max_length=200, null=True)
    country = models.CharField(max_length=50, null=True)
    city = models.CharField(max_length=50, null=True)
    address = models.CharField(max_length=200, null=True)
    date_created = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        return self.first_name
    
class Doctor(models.Model):
    SPECIALTY = (
        ('General doctor', 'General doctor'),
        ('Medical Geneticist', 'Medical Geneticist'),
        ('Rheumatologist','Rheumatologist'),
        ('Neurologist','Neurologist'),
        ('Endocrinologist','Endocrinologist'),
        ('Hematologist','Hematologist'),
        ('Infectious Disease Specialist','Infectious Disease Specialist'),
        ('Immunologist','Immunologist'),
        ('Pulmonologist','Pulmonologist'),
        ('Cardiologist','Cardiologist'),
        ('Dermatologist','Dermatologist'),
        ('Ophthalmologist','Ophthalmologist'),
    )
    STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
    )
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')
    #user = models.OneToOneField(User, null=True, on_delete=models.CASCADE)
    user = models.OneToOneField(User, null=True, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=50, null=True)
    last_name = models.CharField(max_length=50, null=True)
    specialty = models.CharField(max_length=200, null=True, choices=SPECIALTY)
    approval_number = models.CharField(max_length=50, null=True)
    phone = models.CharField(max_length=20, null=True)
    email = models.CharField(max_length=200, null=True)
    country = models.CharField(max_length=50, null=True)
    city = models.CharField(max_length=50, null=True)
    work_address = models.CharField(max_length=200, null=True)
    date_created = models.DateTimeField(auto_now_add=True, null=True)
    patient = models.ForeignKey(Patient, null=True, on_delete= models.SET_NULL)

    def __str__(self):
        return self.first_name

class Prediction(models.Model):
    patient = models.ForeignKey(Patient, null=True, on_delete= models.SET_NULL)
    age = models.FloatField(max_length=50, null=True)
    HbA1c = models.FloatField(max_length=50, null=True)
    birth_weight = models.FloatField(max_length=50, null=True)
    insulin_level = models.FloatField(max_length=50, null=True)
    family_history = models.CharField(max_length=50, null=True)
    developmental_delay = models.CharField(max_length=50, null=True)
    result = models.CharField(max_length=200, null=True)

    def __str__(self):
        return self.result
    
class Appointement(models.Model):
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)
    patient= models.ForeignKey(Patient, on_delete=models.CASCADE)
    date = models.DateField()
    time = models.TimeField()

class Message(models.Model):
    sender = models.ForeignKey(User, related_name='sent_messages', on_delete=models.CASCADE)
    recipient = models.ForeignKey(User, related_name='received_messages', on_delete=models.CASCADE)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Message from {self.sender} to {self.recipient} at {self.timestamp}"
    
