from django.contrib.auth import get_user_model
from leads.models import Employee,Department,Kin,Attendance, Recruitment
from django.contrib.auth.forms import UserCreationForm,AuthenticationForm
from django import forms
from django.core import validators
from django.utils import timezone
from django.db.models import Q
import time
User = get_user_model()

class EmployeeForm (forms.ModelForm):
    first_name = forms.CharField(strip=True, widget=forms.TextInput(attrs={'class':'form-control','placeholder':'First Name'}))
    last_name = forms.CharField(strip=True, widget=forms.TextInput(attrs={'class':'form-control','placeholder':'Last Name'}))
    mobile = forms.CharField(strip=True, widget=forms.TextInput(attrs={'class':'form-control','placeholder':'Mobile Number'}))
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class':'form-control','placeholder':'Valid Email'}))
    emergency = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control','placeholder':'Relative Mobile Number'}))
    gender = forms.ChoiceField(choices=Employee.GENDER,widget=forms.Select(attrs={'class':'form-control'}))
    department = forms.ModelChoiceField(Department.objects.all(),required=True, empty_label='Select a department',widget=forms.Select(attrs={'class':'form-control'}))
    language = forms.ChoiceField(choices=Employee.LANGUAGE,widget=forms.Select(attrs={'class':'form-control'}))
    

    class Meta:
        model = Employee
        fields = ('first_name', 'last_name', 'mobile','email','emergency','salary','gender','department','bank','nuban','language',)
        widgets={
            'salary':forms.TextInput(attrs={'class':'form-control'}),
            'bank':forms.TextInput(attrs={'class':'form-control'}),
            'nuban':forms.TextInput(attrs={'class':'form-control'})
        }

class KinForm(forms.ModelForm):

    first_name = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control'}))
    last_name = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control'}))
    address = forms.CharField(widget=forms.Textarea(attrs={'class':'form-control'}))
    occupation = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control'}))
    mobile = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control'}))
    employee = forms.ModelChoiceField(Employee.objects.filter(kin__employee=None),required=False,widget=forms.Select(attrs={'class':'form-control'}))

    class Meta:
        model = Kin
        fields = '__all__'
    


class DepartmentForm(forms.ModelForm):
    name = forms.CharField(max_length=20, widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Department Name'}))
    history = forms.CharField(max_length=1000, widget=forms.Textarea(attrs={'class':'form-control', 'placeholder':'Brief Department History'}))
    
    class Meta:
        model = Department
        fields = '__all__'

class AttendanceForm(forms.ModelForm):
    status = forms.ChoiceField(choices=Attendance.STATUS,widget=forms.Select(attrs={'class':'form-control w-50'}))
    staff = forms.ModelChoiceField(Employee.objects.filter(Q(attendance__status=None) | ~Q(attendance__date = timezone.localdate())), widget=forms.Select(attrs={'class':'form-control w-50'}))
    class Meta:
        model = Attendance
        fields = ['status','staff']

class RecruitmentForm(forms.ModelForm):
    class Meta:
        model=Recruitment
        fields = '__all__'
        widgets = {
            'first_name':forms.TextInput(attrs={'class':'form-control'}),
            'last_name':forms.TextInput(attrs={'class':'form-control'}),
            'position':forms.TextInput(attrs={'class':'form-control'}),
            'email':forms.EmailInput(attrs={'class':'form-control'}),
            'phone':forms.TextInput(attrs={'class':'form-control'}),
        }
    
        