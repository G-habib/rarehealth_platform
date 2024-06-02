from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('register/', views.register, name='register'),
    path('doctor_request/', views.doctor_request, name='doctor_request'),
    path('registration_status/', views.registration_status, name='registration_status'),
    path('login/', views.loginpage , name="login"),
    path('logout/', views.logoutuser , name="logout"),
]
