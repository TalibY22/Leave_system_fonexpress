from django.contrib import admin
from django.urls import path
from .import views

urlpatterns = [
    path('api/history', views.leave_history),
     path('api/days', views.leave_days),
     path('api/login',views.login_api),
    
]