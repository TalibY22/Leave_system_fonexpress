from django import forms
from.models import Leave,LeaveType,Status

class LeaveForm(forms.ModelForm):
    class Meta:
        model = Leave
        fields = ['leave_type','reason','start_date','end_date','person_covering']
        
        widgets = {
            'start_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'end_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
        }