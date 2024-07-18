

# Create your views here.
from django.shortcuts import render,get_object_or_404
from rest_framework.response import Response
from rest_framework.decorators import api_view
from leave.models import Leave,Employee,leave_balancer
from rest_framework import status

from  .serializers import LeaveSerializer,BalancerSerializer



######################

#Routes specification 





######################


@api_view(['GET'])
def Leave_history(request,employee_id):
       pati =  Leave.objects.filter(id=employee_id)
       serialiser = LeaveSerializer(pati,many=True)
       return Response(serialiser.data)

@api_view(['GET'])
def leave_days(request,employeeid):
       employee = get_object_or_404(Employee, id=employeeid)
       serializer_context = {
            'request': request,
        }
       leave = leave_balancer.objects.filter(employee=employee)
       serialiser = BalancerSerializer(leave,many=True,context=serializer_context)
       return Response(serialiser.data)

