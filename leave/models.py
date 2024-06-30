from typing import Any, Iterable
from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth import get_user

# Create your models here.

class LeaveType(models.Model):
    leave_type = models.CharField(max_length=200)
    Number_of_days  = models.IntegerField()
    
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
    

class Branch(models.Model):
     name = models.CharField(max_length=255)
     location = models.CharField(max_length=255)

     def __str__(self) -> str:
         return self.location



class Employee(models.Model):
      user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    
      department = models.ForeignKey(Department,on_delete=models.CASCADE)
      branch = models.ForeignKey(Branch,on_delete=models.CASCADE)
      
      staff_id=models.IntegerField()
      position = models.CharField(max_length=100)
      First_Name = models.CharField(max_length=100)
      Last_name = models.CharField(max_length=100)
      phone_number = models.IntegerField(unique=True)


      Email = models.EmailField(unique=True)
      start_day = models.DateField(null=True)

      def save(self, *args, **kwargs):
        if not self.user:
            # Create a new User instance
            username = self.First_Name.lower()
            password = "123456789Talib"  # Ensure you handle password securely in production

            # Create the user with the specified password
            self.user = User.objects.create_user(username=username, password=password)
        
        # Save the employee instance before creating leave balances
        super().save(*args, **kwargs)
        
        # Create leave balances after saving employee
        leave_types = LeaveType.objects.all()
        for leave_type in leave_types:
            leave_balancer.objects.get_or_create(employee=self, leave_type=leave_type, defaults={'remaining_days': leave_type.Number_of_days})
      
      def delete(self, *args, **kwargs):
        if self.user:
            self.user.delete()
        super().delete(*args, **kwargs)
          
      def __str__(self) -> str:
          return self.First_Name


#THIS MODEL IS THE ONE WHICH IS RESPONSIBLE  FOR TRACKING LEAVe DAYS

#GET LEAVE_BALANCE  BALANCE WHERE USER = AND LEAVE TYPE IS 
#BELOW IS A CORE MODEL IT WILL HANDLE ALL THE DAYS REMAINING ND ALL
class leave_balancer(models.Model):
      employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
      leave_type = models.ForeignKey(LeaveType, on_delete=models.CASCADE)
      remaining_days = models.IntegerField()
      carry_forward_days = models.IntegerField(default=0)

      def __str__(self) -> str:
        return f"{self.employee.First_Name} {self.leave_type.leave_type}"

      
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
        # Check leave balance
        balance = leave_balancer.objects.get(employee__user=self.user, leave_type=self.leave_type)
        if self.duration > balance.remaining_days:
            raise ValueError(f"Not enough leave balance. Available: {balance.remaining_days}, Requested: {self.duration}")
        super().save(*args, **kwargs)


    # ... Other business fields

    def __str__(self):
        return f"{self.user,self.leave_type}"
    



#IF APPROVED  DEDUCT THE LEAVE DAYS
class Aprroved_leave(models.Model):
      leaveid=models.ForeignKey(Leave,on_delete=models.CASCADE)
      approved_by = models.ForeignKey(User,on_delete=models.CASCADE)
      approved_date = models.DateField(auto_now_add=True)
     
      def save(self, *args, **kwargs):
        # Deduct leave balance
        leave = self.leaveid
        balance = leave_balancer.objects.get(employee__user=leave.user, leave_type=leave.leave_type)
        balance.remaining_days -= leave.duration
        balance.save()
        super().save(*args, **kwargs)
      
      
      def __str__(self) -> str:
          return self.approved_date
