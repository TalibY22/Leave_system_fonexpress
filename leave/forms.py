from django import forms
from.models import Leave,LeaveType,Status,Employee

class LeaveForm(forms.ModelForm):
    class Meta:
        model = Leave
        fields = ['leave_type','reason','start_date','end_date','person_covering','image']
        image = forms.ImageField()
        widgets = {
            'start_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'end_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
        }

  # Adjust import as per your models

class EmployeeForm(forms.ModelForm):
    class Meta:
        model = Employee
        fields = ['staff_id','department','branch' ,'First_Name', 'Last_name', 'phone_number', 'Email']  # Adjusted fields as per your requirement

    def __init__(self, *args, **kwargs):
        super(EmployeeForm, self).__init__(*args, **kwargs)
        self.fields['staff_id'].widget.attrs.update({'class': 'form-control'})
        self.fields['department'].widget.attrs.update({'class': 'form-select'})  # Add Bootstrap form-select class
        self.fields['branch'].widget.attrs.update({'class': 'form-select'})
        self.fields['First_Name'].widget.attrs.update({'class': 'form-control'})  # Add Bootstrap form-control class
        self.fields['Last_name'].widget.attrs.update({'class': 'form-control'})   # Add Bootstrap form-control class
        self.fields['phone_number'].widget.attrs.update({'class': 'form-control'})  # Add Bootstrap form-control class
        self.fields['Email'].widget.attrs.update({'class': 'form-control'})  # Add Bootstrap form-control class
