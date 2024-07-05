from django.shortcuts import render,get_object_or_404,redirect,HttpResponse
from django.db.models import Sum
from django.db.models import Q
from .forms import LeaveForm,EmployeeForm
from django.contrib.auth.decorators import login_required, user_passes_test
from .models import Leave,Status,leave_balancer,Employee,LeaveType,Approved_leave,Department,Branch
from django.contrib.auth.models import User
from django.core.mail import send_mail
from .blah import send_email
from datetime import datetime, timedelta
from django.utils import timezone
from concurrent.futures import ThreadPoolExecutor
from django.http import JsonResponse


from datetime import date 

#Test to dtermine if user is a manager or not !!!!Very important entire security relies on this code 
def is_manager(user):
    return user.groups.filter(name='Manager').exists()

# Create your views here.
@login_required
def home(request):
    if is_manager(user=request.user):
         
         
         
         upcoming_leaves=Leave.objects.filter(start_date__gt=date.today()).count()
         rejected_leaves =Leave.objects.filter(status_id=3).count()
         requests =Leave.objects.filter(status_id=1).count()

         employee_on_leave2 = Leave.objects.filter(start_date__lte=date.today(),status_id=2, end_date__gte=date.today()).count()
         employee_on_leave = Leave.objects.filter(start_date__lte=date.today(),status_id=2, end_date__gte=date.today())
         

         
         
         
     
         return render(request,"leave/admin/admin_dashboard.html",{"leaves":employee_on_leave,"upcoming_leaves":upcoming_leaves,"rejected_leaves":rejected_leaves,"employees_on_leave":employee_on_leave2,"leave_request":requests})
    else:
       
       employee = get_object_or_404(Employee, user=request.user)
       leaves_taken = Leave.objects.filter(employee=employee,status_id=2).count()
       
    
    
       Total_off_days = Approved_leave.objects.filter(leaveid__employee=employee).aggregate(total_days=Sum('leaveid__duration'))['total_days']
       sick_leaves_taken = Approved_leave.objects.filter(leaveid__employee=employee,leaveid__leave_type=4).aggregate(total_days=Sum('leaveid__duration'))['total_days']
       compulsory_leave_days = Approved_leave.objects.filter(leaveid__employee=employee,leaveid__leave_type=8).aggregate(total_days=Sum('leaveid__duration'))['total_days']
       
       general_leave_days = Approved_leave.objects.filter(leaveid__employee=employee,leaveid__leave_type=5).aggregate(total_days=Sum('leaveid__duration'))['total_days']
    
       Leave_balance_compulsory = leave_balancer.objects.get(employee=employee,leave_type=8)
       sick_balance = leave_balancer.objects.get(employee=employee,leave_type=4)
    
       compulsory_days_available = Leave_balance_compulsory.remaining_days
       sick_days_available = sick_balance.remaining_days
    
    
    
    
    
    
    
       context = {
        'offdays':leaves_taken,
        'paid_leave':compulsory_days_available,
        'sick_days':sick_leaves_taken,
        'paid_leaves_taken':compulsory_leave_days,

        
       }

    

         

       return render(request,"leave/home.html",context)

@login_required
def apply_leave(request):
        employee = Employee.objects.get(user=request.user)
        if request.method=='POST':
            form = LeaveForm(request.POST,request.FILES)
            if form.is_valid():
                new_leave = form.save(commit=False)
               
                new_leave.employee = employee
                balance = leave_balancer.objects.get(employee__user=request.user, leave_type=new_leave.leave_type)
                total_available_days = balance.remaining_days
                duration = (new_leave.end_date - new_leave.start_date).days + 1
               
               
                if duration > total_available_days:
                   error_message = f"Not enough leave balance. Available: {total_available_days}, Requested: {duration}"
                   return render(request, 'leave/apply.html', {"form": form, "fail": error_message})
                new_leave.save()

                send_mail(
           "A new leave request has been made ",
             " A leave request has been made",
            "foneexpress@gmail.com",
            ["yakubtalib70@gmail.com"],
            fail_silently=False,
          )

                
                return render(request,'leave/apply.html',{"form":LeaveForm(),"success":True})
        
        
        Leave_balance_compulsory = leave_balancer.objects.get(employee=employee,leave_type=8)
        sick_balance = leave_balancer.objects.get(employee=employee,leave_type=4)
    
        compulsory_days_available = Leave_balance_compulsory.remaining_days
        sick_days_available = sick_balance.remaining_days
        
        
        return render(request,'leave/apply.html',{"form":LeaveForm,"available_annual_leave":compulsory_days_available,"available_sick_leave":sick_days_available})    


@login_required
def user_leaves(request):
     employee = get_object_or_404(Employee, user=request.user)
     leaves =Leave.objects.filter(employee=employee)

     return render(request,'leave/leave_history.html',{"leaves":leaves})


######################
     #ADMIN VIEWS
######################
@login_required
@user_passes_test(is_manager)
def view_all_leaves(request):
     
   
       

     
     
     leaves = Leave.objects.filter(status_id=1)

     return render(request,'leave/admin/view_all_leaves.html',{"leaves":leaves})




@login_required
@user_passes_test(is_manager)
def view_accepted_leaves(request):
     leaves = Leave.objects.filter(status_id=2)
     departments = Department.objects.all()
     branches = Branch.objects.all()
      
      #CODE NEEDS TO BE REWRITTEN
     if request.method=='POST':
        
      
        date = request.POST.get('date')
        department_id = request.POST.get('department')
        branch_id = request.POST.get('branch')
        
        # Use the filters if they are provided
        query = Q()

    # Conditionally add filters to the Q object
        if date:
         query &= Q(start_date=date)
        if department_id:
         query &= Q(employee__department__name=department_id)
        if branch_id:
         query &= Q(employee__branch__name=branch_id)

    # Apply the Q object to your queryset
        leaves = Leave.objects.filter(query)
        print(leaves)
        return render(request,'leave/admin/accepted_leaves.html',{"leaves":leaves,"departments":departments,"branches":branches})
     
     
     
     

    


     return render(request,'leave/admin/accepted_leaves.html',{"leaves":leaves,"departments":departments,"branches":branches})


@login_required
@user_passes_test(is_manager)
def view_rejected_leaves(request):
     leaves = Leave.objects.filter(status_id=3)

     return render(request,'leave/admin/rejected_leaves.html',{"leaves":leaves})

#Change above code to one function 




@login_required
@user_passes_test(is_manager)
def reject_leave(request, id):
    leave = get_object_or_404(Leave, id=id)

    if request.method == 'POST':
        
        reason = request.POST.get('reason')

        rejected_status = Status.objects.get(status='Rejected')
        leave.status = rejected_status
        
        leave.save()
        
        subject = "Leave Rejected"
        message = reason
        from_email = "foneexpress@gmail.com"
        recipient_list = ["yakubtalib70@gmail.com"]
        # MY FUTURE SELF THIS WHERE UR MESSAGE CODE GOES DONT MESS THIS UP
        
        with ThreadPoolExecutor() as executor:
            executor.submit(send_email, subject, message, from_email, recipient_list)
      
        return redirect('view_all_leaves')  

@login_required
#MY SEXY FUTURE SELF MAKE SURE U ADD CODE TO SUBTRACT DAYS IF ITS PAID LEAVE
@user_passes_test(is_manager) 
def Accept_leave(request, id):
    leave = get_object_or_404(Leave, id=id)

    if request.method == 'POST':
      
        accepted_status = Status.objects.get(status='Accepted')
        
        leave.status = accepted_status
       
        leave.save()
        Approved_leave.objects.create(leaveid=leave, approved_by=request.user)
       

       
       
       
        send_mail(
           "Leave accepted",
           "U may proceed to have a leave on the date specified",
            "foneexpress@gmail.com",
            ["yakubtalib70@gmail.com"],
            fail_silently=False,
        ) 

        

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





######
#VIEW FOR SHOWING USER HISTORY
######
@login_required
@user_passes_test(is_manager)
#Make sure u retrieve data according to financial year
def leave_history(request,id):
    
    Total_off_days = Leave.objects.filter(employee_id=id,status_id=2).aggregate(total_days=Sum('duration'))['total_days']

    leaves_taken = Leave.objects.filter(employee_id=id)
    employee = get_object_or_404(Employee, id=id)
    username = employee.First_Name
    
    
    Total_off_days = Approved_leave.objects.filter(leaveid__employee_id=id).aggregate(total_days=Sum('leaveid__duration'))['total_days']
    sick_leaves_taken = Approved_leave.objects.filter(leaveid__employee_id=id,leaveid__leave_type=4).aggregate(total_days=Sum('leaveid__duration'))['total_days']
    compulsory_leave_days = Approved_leave.objects.filter(leaveid__employee_id=id,leaveid__leave_type=8).aggregate(total_days=Sum('leaveid__duration'))['total_days']
    general_leave_days = Approved_leave.objects.filter(leaveid__employee_id=id,leaveid__leave_type=5).aggregate(total_days=Sum('leaveid__duration'))['total_days']
    
    Leave_balance_compulsory = leave_balancer.objects.get(employee=employee,leave_type=8)
    sick_balance = leave_balancer.objects.get(employee=employee,leave_type=4)
    
    compulsory_days_available = Leave_balance_compulsory.remaining_days
    sick_days_available = sick_balance.remaining_days
    
    
    success = False
    if Total_off_days is None:
        success = True 
    
    
    
    
    
    context = {
        'compulsory_days_available':compulsory_days_available,
        'leaves':leaves_taken,
        'employee': username,
        'sick_days_taken':sick_leaves_taken,
        'total_leaves': Total_off_days,
        'success':success,
        'sick_days_remaining':sick_days_available,
        'compulsory_days':compulsory_leave_days,
        'general_days':general_leave_days
    }

    
  

    
    
    return render(request, 'leave/admin/employee_history.html',context)

@login_required
@user_passes_test(is_manager)
def list_employees(request):
    user = Employee.objects.all()
    if request.method == 'POST':
         form = EmployeeForm(request.POST)
         if form.is_valid():
            form.save()
            return render(request, 'leave/admin/employees.html',{'users':user,'form':EmployeeForm()})



               
   
    return render(request, 'leave/admin/employees.html',{'employees':user,'form':EmployeeForm()})




@login_required
@user_passes_test(is_manager)
def simple_employee_search(request):
    query = request.GET.get("query")
    results = []
    if query:
        results=Employee.objects.filter(
          Q(First_Name__icontains=query) |
          Q(Last_name__icontains=query)
        
        )
        return render(request,"leave/admin/employees.html",{"employees":results,"form":EmployeeForm()})





@login_required
@user_passes_test(is_manager)
def search_employees(request):
    if 'term' in request.GET:
        qs = User.objects.filter(First_Name__icontains=request.GET.get('term'))
        names = list()
        for employee in qs:
            names.append(employee.First_Name + ' ' + employee.Last_name)
        return JsonResponse(names, safe=False)
    return render(request, 'search.html')



@login_required
@user_passes_test(is_manager)
def Delete_leave_record(request,id):
     if request.method =='POST':
          record = Leave.objects.filter(id=id)
          record.delete()

          return redirect('rejected_leaves')

