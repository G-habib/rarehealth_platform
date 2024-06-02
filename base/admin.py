from django.contrib import admin
from django.contrib.auth.models import User
from .models import *

# Register your models here.
admin.site.register(Patient)
admin.site.register(Prediction)
admin.site.register(Appointement)
admin.site.register(Message)

@admin.action(description='Approve selected doctors')
def approve_doctors(modeladmin, request, queryset):
    queryset.update(status='approved')
    for doctor in queryset:
        user = User.objects.create_user(
            username=doctor.email,
            email=doctor.email,
            first_name=doctor.first_name,
            last_name=doctor.last_name,
            password=User.objects.make_random_password()
        )
        doctor.user = user
        doctor.save()

@admin.register(Doctor)
class DoctorAdmin(admin.ModelAdmin):
    list_display = ('user','first_name', 'last_name', 'email', 'specialty', 'approval_number', 'work_address', 'status')
    actions = [approve_doctors]
