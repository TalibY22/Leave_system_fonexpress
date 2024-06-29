from typing import Any
from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth import get_user

# Create your models here.

class LeaveType(models.Model):
    leave_type = models.CharField(max_length=200)
    Number_of_days  = models.IntegerField
    
    def __str__(self):
        return self.leave_type








class Status(models.Model):
      status = models.CharField(max_length=255)

      def __str__(self):
        return self.status



class Department(models.Model):
    name = models.CharField(max_length=255)
    
    def __str__(self) -> str:
        return self.name
    

class Employee(models.Model):
      user_id = models.ForeignKey(User,on_delete=models.CASCADE)
      department = models.ForeignKey(Department,on_delete=models.CASCADE)
      First_Name = models.CharField(max_length=100)
      Last_name = models.CharField(max_length=100)
      Email = models.EmailField(unique=True)


#THIS MODEL IS THE ONE WHICH IS RESPONSIBLE  FOR TRACKING LEAVe DAYS

#GET LEAVE_BALANCE  BALANCE WHERE USER = AND LEAVE TYPE IS 
#BELOW IS A CORE MODEL IT WILL HANDLE ALL THE DAYS REMAINING ND ALL
class leave_balancer(models.Model):
      employee = models.OneToOneField(Employee, on_delete=models.CASCADE)
      leave_type = models.ForeignKey(LeaveType, on_delete=models.CASCADE)
      remaining_days = models.IntegerField()

      def __str__(self) -> str:
          return self.remaining_days

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
    



#IF APPROVED  DEDUCT THE LEAVE DAYS
class Aprroved_leave(models.Model):
      leaveid=models.ForeignKey(Leave,on_delete=models.CASCADE)
      approved_by = models.ForeignKey(User,on_delete=models.CASCADE)
      approved_date = models.DateField(auto_now_add=True)

      def __str__(self) -> str:
          return self.approved_date
