from django.contrib import admin

# Register your models here.
from .models import Leave,LeaveType,Status

admin.site.register(Leave)
admin.site.register(LeaveType)
admin.site.register(Status)