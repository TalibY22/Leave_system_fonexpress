# signals.py
from django.db.models.signals import post_save,pre_delete
from django.dispatch import receiver
from datetime import date
from .models import Leave, Status,Employee,leave_balancer,LeaveType






@receiver(post_save, sender=Employee)
def create_leave_balance(sender, instance, created, **kwargs):
    if created:
        leave_types = LeaveType.objects.all()
        for leave_type in leave_types:
            LeaveType.objects.create(employee=instance, leave_type=leave_type, remaining_days=leave_type.allowed_days)

@receiver(pre_delete, sender=Leave)
def create_leave_balance(sender, instance, created, **kwargs):
    if created:
        leave_types = LeaveType.objects.all()
        for leave_type in leave_types:
            LeaveType.objects.create(employee=instance, leave_type=leave_type, remaining_days=leave_type.allowed_days)
