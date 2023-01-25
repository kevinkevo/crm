from django.shortcuts import render,redirect, resolve_url,reverse, get_object_or_404
from django.urls import reverse_lazy
from django.contrib.auth import get_user_model
from leads.models  import Employee, Department,Kin, Attendance, Recruitment
from django.contrib.auth.views import LoginView
from django.contrib.auth import logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import FormView, CreateView,View,DetailView,TemplateView,ListView,UpdateView,DeleteView
from .forms import EmployeeForm,KinForm,DepartmentForm,AttendanceForm,  RecruitmentForm
from django.core.exceptions import ObjectDoesNotExist
from django.contrib import messages
from django.utils import timezone
from django.db.models import Q
from django.contrib import messages

from .mixins import OrganisorAndLoginRequiredMixin


# Create your views here.


 # Main Board   
class Dashboard(LoginRequiredMixin,ListView):
    template_name = 'hrms/dashboard/index.html'
    model = get_user_model()
    context_object_name = 'qset'            
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs) 
        context['emp_total'] = Employee.objects.all().count()
        context['dept_total'] = Department.objects.all().count()
        context['admin_count'] = get_user_model().objects.all().count()
        context['workers'] = Employee.objects.order_by('-id')
        return context



# Employee's Controller
class Employee_New(OrganisorAndLoginRequiredMixin,CreateView):
    model = Employee  
    form_class = EmployeeForm  
    template_name = 'hrms/employee/create.html'
    redirect_field_name = 'redirect:'
    
    
class Employee_All(OrganisorAndLoginRequiredMixin,ListView):
    template_name = 'hrms/employee/index.html'
    model = Employee
    context_object_name = 'employees'
    paginate_by  = 5
    
class Employee_View(OrganisorAndLoginRequiredMixin,DetailView):
    queryset = Employee.objects.select_related('department')
    template_name = 'hrms/employee/single.html'
    context_object_name = 'employee'

    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        try:
            query = Kin.objects.get(employee=self.object.pk)
            context["kin"] = query
            return context
        except ObjectDoesNotExist:
            return context
        
class Employee_Update(OrganisorAndLoginRequiredMixin,UpdateView):
    model = Employee
    template_name = 'hrms/employee/edit.html'
    form_class = EmployeeForm
    
    
    
class Employee_Delete(OrganisorAndLoginRequiredMixin,DeleteView):
    pass

class Employee_Kin_Add (OrganisorAndLoginRequiredMixin,CreateView):
    model = Kin
    form_class = KinForm
    template_name = 'hrms/employee/kin_add.html'
    
   

    def get_context_data(self):
        context = super().get_context_data()
        if 'id' in self.kwargs:
            emp = Employee.objects.get(pk=self.kwargs['id'])
            context['emp'] = emp
            return context
        else:
            return context

class Employee_Kin_Update(OrganisorAndLoginRequiredMixin,UpdateView):
    model = Kin
    form_class = KinForm
    template_name = 'hrms/employee/kin_update.html'
    

    def get_initial(self):
        initial = super(Employee_Kin_Update,self).get_initial()
        
        if 'id' in self.kwargs:
            emp =  Employee.objects.get(pk=self.kwargs['id'])
            initial['employee'] = emp.pk
            
            return initial

#Department views

class Department_Detail(OrganisorAndLoginRequiredMixin, ListView):
    context_object_name = 'employees'
    template_name = 'hrms/department/single.html'
    
    def get_queryset(self): 
        queryset = Employee.objects.filter(department=self.kwargs['pk'])
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["dept"] = Department.objects.get(pk=self.kwargs['pk']) 
        return context
    
    


class Department_New (OrganisorAndLoginRequiredMixin,CreateView):
    model = Department
    template_name = 'hrms/department/create.html'
    form_class = DepartmentForm
   

class Department_Update(OrganisorAndLoginRequiredMixin,UpdateView):
    model = Department
    template_name = 'hrms/department/edit.html'
    form_class = DepartmentForm
    
    success_url = reverse_lazy('hrms:dashboard')

#Attendance View

class Attendance_New (OrganisorAndLoginRequiredMixin,CreateView):
    model = Attendance
    form_class = AttendanceForm
    template_name = 'hrms/attendance/create.html'
    success_url = reverse_lazy('hrms:attendance_new')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["today"] = timezone.localdate()
        pstaff = Attendance.objects.filter(Q(status='PRESENT') & Q (date=timezone.localdate())) 
        context['present_staffers'] = pstaff
        return context

class Attendance_Out(OrganisorAndLoginRequiredMixin,View):

    def get(self, request,*args, **kwargs):

       user=Attendance.objects.get(Q(staff__id=self.kwargs['pk']) & Q(status='PRESENT')& Q(date=timezone.localdate()))
       user.last_out=timezone.localtime()
       user.save()
       return redirect('hrms:attendance_new')   



class Payroll(OrganisorAndLoginRequiredMixin, ListView):
    model = Employee
    template_name = 'hrms/payroll/index.html'
    context_object_name = 'stfpay'



def recruitment_creation(request):
	if not request.user.is_authenticated:
		return redirect('registration:login')
	if request.method == 'POST':
		form = RecruitmentForm(data = request.POST)
		if form.is_valid():
			instance = form.save(commit = False)
			user = request.user
			instance.user = user
			instance.save()


			# print(instance.defaultdays)
			messages.success(request,'Application sent,wait for response',extra_tags = 'alert alert-success alert-dismissible show')
			return redirect('hrms:recruitment')

		messages.error(request,'Application failed,please try again later',extra_tags = 'alert alert-warning alert-dismissible show')
		return redirect('hrms:recruitment')


	dataset = dict()
	form = RecruitmentForm()
	dataset['form'] = form
	dataset['title'] = 'Apply for position'
	return render(request,'hrms/recruitment/index.html',dataset)
	


class RecruitmentAll(OrganisorAndLoginRequiredMixin,ListView):
    model = Recruitment
    template_name = 'hrms/recruitment/all.html'
    context_object_name = 'recruit'

class RecruitmentDelete (OrganisorAndLoginRequiredMixin,View):
    def get (self, request,pk):
     form_app = Recruitment.objects.get(pk=pk)
     form_app.delete()
     return redirect('hrms:recruitmentall', permanent=True)

class Pay(OrganisorAndLoginRequiredMixin,ListView):
    model = Employee
    template_name = 'hrms/payroll/index.html'
    context_object_name = 'emps'
   

