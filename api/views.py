

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
    


   

@api_view(['POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def leave_request(request):
    serializer = LeaveSerializer(data=request.data)
    if serializer.is_valid():
        #data added manually 
        
        employee = get_object_or_404(Employee, user=request.user)



        #Data acquired from the serializer
        leave_type = serializer.validated_data['leave_type']
        reason = serializer.validated_data['reason']
        start_date = serializer.validated_data['start_date']
        end_date = serializer.validated_data['end_date']
        person_covering = serializer.validated_data['person_covering']
        duration = 3
         
        leave = Leave(
            employee=employee,
            leave_type=leave_type,
            reason=reason,
            start_date=start_date,
            end_date=end_date,
            person_covering=person_covering,
            
            duration=duration
        )
        
        # Save the leave instance to the database
        leave.save()

        return Response({"success": "Leave request submitted successfully"}, status=status.HTTP_201_CREATED)
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
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def leave_days(request):
       
       employee = get_object_or_404(Employee, user=request.user)
       serializer_context = {
            'request': request,
        }
       leave = leave_balancer.objects.filter(employee=employee)
       serialiser = BalancerSerializer(leave,many=True,context=serializer_context)
       return Response(serialiser.data)

