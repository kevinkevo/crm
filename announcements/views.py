from django.shortcuts import render

# Create your views here.
from django.shortcuts import render
from django.core.files.storage import FileSystemStorage
import os, datetime
from django.shortcuts import reverse
from django.urls import reverse_lazy
from django.contrib import admin
from django.views.generic import FormView, CreateView,View,DetailView,TemplateView,ListView,UpdateView,DeleteView
from leads.models import Announcement
from django.contrib.auth.mixins import LoginRequiredMixin
from hrms.mixins import OrganisorAndLoginRequiredMixin
from .forms import AnnouncementForm
from django.shortcuts import render,redirect,get_object_or_404
from django.conf import settings
User = settings.AUTH_USER_MODEL
from django.core.mail import send_mail
from django.contrib import messages
from django.contrib.auth import get_user_model

User = get_user_model()
     

def announcement_creation(request):
	if not request.user.is_authenticated:
		return redirect('registration:login')
	if request.method == 'POST':
		form =  AnnouncementForm(data = request.POST)
		if form.is_valid():
			instance = form.save(commit = False)
			user = request.user
			instance.user = user
			instance.save()


			# print(instance.defaultdays)
			messages.success(request,'announcement Sent,click me to check',extra_tags = 'alert alert-success alert-dismissible show')
			return redirect('announcements:announcement')

		messages.error(request,'failed to sent announcement,please try again ',extra_tags = 'alert alert-warning alert-dismissible show')
		return redirect('announcements:announcement')


	dataset = dict()
	form =  AnnouncementForm()
	dataset['form'] = form
	dataset['title'] = 'create announcement'
	return render(request,'file/index.html',dataset)

def announcement_all(request):
	
	announcements = Announcement.objects.all()
	return render(request,'file/all.html',{'announcement_all':announcements,'title':'announcement'})


    
class AnnouncementDelete (OrganisorAndLoginRequiredMixin,View):
    def get (self, request,pk):
     form_app = Announcement.objects.get(pk=pk)
     form_app.delete()
     return redirect('announcements:announcementall', permanent=True)

    

 