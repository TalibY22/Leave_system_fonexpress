from django.contrib import admin

# Register your models here.
from .models import Leave,LeaveType,Status,Employee,leave_balancer,Department,Branch

admin.site.register(Leave)
admin.site.register(LeaveType)
admin.site.register(Status)
admin.site.register(Employee)
admin.site.register(leave_balancer)
admin.site.register(Department)
admin.site.register(Branch)