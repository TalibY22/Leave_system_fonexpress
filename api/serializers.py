from leave.models import Leave,Approved_leave,leave_balancer
from rest_framework import serializers
from django.contrib.auth.models import Group, User

class LeaveSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Leave
        fields = ['leave_type', 'reason', 'start_date', 'end_date','person_covering']

class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ['url', 'username', 'email', 'groups']


class BalancerSerializer(serializers.HyperlinkedModelSerializer):
    
    class Meta:
     model = leave_balancer
    
     fields = ['leave_type','remaining_days','carry_forward_days']