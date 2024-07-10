

# Create your views here.
from django.shortcuts import render
from django_rest.res import Response
from rest_framework.decorators import api_view
from rest_framework import status
from .models import Patients,Doctors,Nurse
from  .serializers import PatientSerializer,DoctorsSerializer