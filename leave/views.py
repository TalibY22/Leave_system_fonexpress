from django.shortcuts import render,get_object_or_404,redirect
from .forms import LeaveForm
from django.contrib.auth.decorators import login_required, user_passes_test
from .models import Leave,Status
from datetime import date 


def is_manager(user):
    return user.groups.filter(name='Manager').exists()

# Create your views here.
@login_required
def home(request):
    if is_manager(user=request.user):
         return render(request,"leave/admin/admin_base.html")
    return render(request,"leave/home.html")

@login_required
def apply_leave(request):
        if request.method=='POST':
            form = LeaveForm(request.POST)
            if form.is_valid():
                new_leave = form.save(commit=False)
                new_leave.user = request.user
                new_leave.save()
                return render(request,'leave/apply.html',{"form":LeaveForm(),"success":True})
        return render(request,'leave/apply.html',{"form":LeaveForm})    




######################
     #ADMIN VIEWS
######################
@login_required
@user_passes_test(is_manager)
def view_all_leaves(request):
     leaves = Leave.objects.filter(status_id=1)

     return render(request,'leave/admin/view_all_leaves.html',{"leaves":leaves})

def view_accepted_leaves(request):
     leaves = Leave.objects.filter(status_id=2)

     return render(request,'leave/admin/accepted_leaves.html',{"leaves":leaves})

def view_rejected_leaves(request):
     leaves = Leave.objects.filter(status_id=3)

     return render(request,'leave/admin/rejected_leaves.html',{"leaves":leaves})

#Change above code to one function 




@login_required
def reject_leave(request, id):
    leave = get_object_or_404(Leave, id=id)

    if request.method == 'POST':
      
        rejected_status = Status.objects.get(status='Rejected')
        leave.status = rejected_status
        leave.save()

        # MY FUTURE SELF THIS WHERE UR MESSAGE CODE GOES DONT MESS THIS UP

      
        return redirect('view_all_leaves')  

@login_required
def Accept_leave(request, id):
    leave = get_object_or_404(Leave, id=id)

    if request.method == 'POST':
      
        accepted_status = Status.objects.get(status='Accepted')
        leave.status = accepted_status
        leave.save()

        # MY FUTURE SELF THIS WHERE UR MESSAGE CODE GOES DONT MESS THIS UP

      
        return redirect('view_all_leaves')  
    
@login_required
@user_passes_test(is_manager)
def active_leaves(request):
    current_date = date.today()
    leaves_on_date = Leave.objects.filter(start_date__lte=current_date,status_id=2, end_date__gte=current_date)

    if not leaves_on_date.exists():
         return render(request, 'leave/admin/active_leaves.html', {'success': True})
         

    return render(request, 'leave/admin/active_leaves.html', {'leaves': leaves_on_date})