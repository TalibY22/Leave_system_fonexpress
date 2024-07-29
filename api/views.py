

# Create your views here.
from django.shortcuts import render,get_object_or_404
from rest_framework.response import Response
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from leave.models import Leave,Employee,leave_balancer
from rest_framework import status
from rest_framework.authtoken.models import Token
from  .serializers import LeaveSerializer,BalancerSerializer,LoginSerializer
from django.contrib.auth import authenticate
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication


######################

#Routes specification 





######################

@api_view(['POST'])
def login_api(request):
    serializer = LoginSerializer(data=request.data)
    if serializer.is_valid():
        username = serializer.validated_data['username']
        password = serializer.validated_data['password']
        user = authenticate(username=username, password=password)
        if user:
            token, created = Token.objects.get_or_create(user=user)
            return Response({'token': token.key})
        else:
            return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)
    else:
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def leave_history(request):

    employee = get_object_or_404(Employee, user=request.user)
    leave_records = Leave.objects.filter(employee=employee)
    serializer = LeaveSerializer(leave_records, many=True)
    return Response(serializer.data)




@api_view(['GET'])
def leave_days(request,employeeid):
       employee = get_object_or_404(Employee, id=employeeid)
       serializer_context = {
            'request': request,
        }
       leave = leave_balancer.objects.filter(employee=employee)
       serialiser = BalancerSerializer(leave,many=True,context=serializer_context)
       return Response(serialiser.data)

