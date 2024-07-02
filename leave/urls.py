from django.contrib import admin
from django.urls import path,include
from . import views 
from django.conf import settings

from django.conf.urls.static import static

urlpatterns = [
    path("", views.home,name="home"),
    path("apply/", views.apply_leave,name="apply"),
    path("leaves/", views.user_leaves,name="records"),









   path("manager/view_leaves",views.view_all_leaves,name="view_all_leaves"),
   path("manager/accepted_leaves",views.view_accepted_leaves,name="accepted_leaves"),
   path("manager/rejected_leaves",views.view_rejected_leaves,name="rejected_leaves"),
   path("manager/active_leaves",views.active_leaves,name="active"),
   path("manager/employees",views.list_employees,name="employee"),
   path("manager/search",views.simple_employee_search,name="search_employee"),
   
   
   
   path("manager/reject/<int:id>",views.reject_leave,name="reject"),
   path("manager/accept/<int:id>",views.Accept_leave,name="accept"),
   path("manager/history/<int:id>",views.leave_history,name="history"),
   
    path("manager/delete/<int:id>",views.Delete_leave_record,name="delete"),
]
