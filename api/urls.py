from django.contrib import admin
from django.urls import path
from .import views

urlpatterns = [
    path('api/history', views.leave_history),
     path('api/days', views.leave_days),
     path('api/login',views.login_api),
     #Path for applying for leave try it out in the post leave form
     path('api/apply' ,views.leave_request),
    
]