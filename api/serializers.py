from leave.models import Leave,Approved_leave,leave_balancer,LeaveType
from rest_framework import serializers
from django.contrib.auth.models import Group, User

class LeaveSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Leave
        fields = ['leave_type', 'reason', 'start_date', 'end_date','person_covering']


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()



class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ['username','password']


class BalancerSerializer(serializers.ModelSerializer):
    leave_type = serializers.PrimaryKeyRelatedField(queryset=LeaveType.objects.all())
    class Meta:
     model = leave_balancer
    
     fields = ['leave_type','remaining_days','carry_forward_days']