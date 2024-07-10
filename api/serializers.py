from leave.models import Leave,Approved_leave
from django_rest import serializers
from django.contrib.auth.models import Group, User

class LeaveSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Leave
        fields = ['leave_type', 'reason', 'start_date', 'end_date','person_covering']

class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ['url', 'username', 'email', 'groups']
