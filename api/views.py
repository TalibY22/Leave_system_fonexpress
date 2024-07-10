

# Create your views here.
from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.decorators import api_view
from leave.models import Leave,Employee,leave_balancer
from rest_framework import status

from  .serializers import LeaveSerializer,BalancerSerializer


@api_view(['GET'])
def Leave_history(request,employee_id):
       pati =  Leave.objects.filter(id=employee_id)
       serialiser = LeaveSerializer(pati,many=True)
       return Response(serialiser.data)

@api_view(['GET'])
def leave_days(request,employeeid):
       leave = leave_balancer.objects.filter(employee__id=employeeid)
       serialiser = BalancerSerializer(leave,many=True)
       return Response(serialiser.data)