from django.contrib import admin
from django.urls import path,include
from . import views
from django.contrib.auth.views import LoginView,LogoutView



urlpatterns = [
     path('login/', LoginView.as_view(), name='login'),
     path('logout/', LogoutView.as_view(), name='logout'),
     path('password/', views.change_password, name='change_password'),
]