from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('diseases/', views.diseases_view, name='diseases'),
    path('treatment/', views.treatment_view, name='treatment'),
    path('patients/', views.patients_view, name='patients'),
    path('doctors/', views.doctors_view, name='doctors'),
    path('location/', views.location_view, name='location'),
    path('view_appointment/', views.appointment_view, name='view_appointment'),
    path('view_doc_appointment/', views.doc_appointment_view, name='view_doc_appointment'),
    path('add_appointment/', views.add_appointment, name='add_appointment'),
    path('delete_appointment(?A<int:aid>)/', views.delete_appointment, name='delete_appointment'),
    path('delete_doc_appointment(?A<int:aid>)/', views.delete_doc_appointment, name='delete_doc_appointment'),
    path('patients_msg/', views.patients_msg_view, name='patients_msg'),
    path('doctors_msg/', views.doctors_msg_view, name='doctors_msg'),
]
