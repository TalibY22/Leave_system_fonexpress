from typing import Any
from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth import get_user

# Create your models here.

class LeaveType(models.Model):
    leave_type = models.CharField(max_length=200)
    # ... Other business fields

    def __str__(self):
        return self.leave_type


class Status(models.Model):
      status = models.CharField(max_length=255)

      def __str__(self):
        return self.status





class Leave(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # Foreign key to User
    leave_type = models.ForeignKey(LeaveType,on_delete=models.CASCADE)
    reason = models.CharField(max_length=255)
    start_date = models.DateField()
    end_date = models.DateField()
    person_covering = models.CharField(max_length=255)
    status = models.ForeignKey(Status,on_delete=models.CASCADE,default=1)
    duration=models.IntegerField()
     
    def save(self, *args, **kwargs):
        self.duration = (self.end_date - self.start_date).days + 1
        super().save(*args, **kwargs)


    # ... Other business fields

    def __str__(self):
        return f"{self.user,self.leave_type}"