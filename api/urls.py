from django.contrib import admin
from django.urls import path
from .import views

urlpatterns = [
    path('api/history/<int:employee_id>', views.Leave_history),
     path('api/days/<int:employeeid>', views.leave_days),
    
]