from multiprocessing import context
from unicodedata import category
from django.shortcuts import render,redirect, reverse
from django.views import generic
from .models import Category, Lead, Agent,Category
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import  LeadModelForm,CustomUserCreationForm,LeadCategoryUpdateForm
from django.core.mail import send_mail
from django.contrib.auth import get_user_model
from django.urls import reverse_lazy
from agents.mixins import OrganisorAndLoginRequiredMixin # the mixins set access to differnt users




# Create your views here.

#class SignupView(generic.CreateView):
	#template_name = "registration/signup.html"
	#form_class = CustomUserCreationForm

	#def get_success_url(self):
		#return reverse("leads")

class SignupView(generic.CreateView):
    form_class = CustomUserCreationForm
    success_url = reverse_lazy('login')
    template_name = "registration/signup.html"


class LandingPageView( generic.TemplateView):
	template_name = "landing.html"
	
class LandPageView( generic.TemplateView):
	template_name = "landpage.html"


class LeavePageView( generic.TemplateView):
	template_name = "leave/leaves.html"

class LeadListView(LoginRequiredMixin, generic.ListView):
	template_name = "lead_list.html"
	
	context_object_name = "leads"

	def get_queryset(self):
		user = self.request.user
		if user.is_organisor:
			#if you are an organisor you see all leeds
			queryset= Lead.objects.filter()		
		else:
			#agent only see leeds that are assigned to them
			queryset= Lead.objects.filter()
			
		return queryset	

class LeadDetailView(LoginRequiredMixin, generic.DetailView):
	template_name = "lead_detail.html"
	context_object_name = "lead"

	def get_queryset(self):
		user = self.request.user
		

		if user.is_organisor:
			#if you are an organisor you see all leeds
			queryset= Lead.objects.filter()
			
		else:
			#agent only see leeds that are assigned to them
			queryset= Lead.objects.filter()
			#queryset= queryset.fliter(agent__user=user)
		return queryset


class LeadCreateView(OrganisorAndLoginRequiredMixin, generic.CreateView):# agent cannot create a lead
	template_name = "lead_create.html"
	form_class = LeadModelForm

	def  get_success_url(self):
		return reverse("leads:lead-list")


	def form_valid(self, form):
		lead= form.save(commit=False)
		
		lead.organisation = self.request.user.userprofile
		lead.save()
		send_mail(
			subject = "A ticket has been created!!",
			message = "Go to the site to  view. Thank you",
			from_email = "kevindev@gmail.com",
			recipient_list = [lead.agent],
		)
		return super(LeadCreateView, self).form_valid(form)	


 


class LeadUpdateView(OrganisorAndLoginRequiredMixin, generic.UpdateView):# agent cannot update the lead
	template_name = "lead_update.html"
	form_class = LeadModelForm

	def get_queryset(self):
		user = self.request.user	
		#organisor only can update a lead
		return  Lead.objects.filter()
	def  get_success_url(self):
		return reverse("leads:lead-list")

	

class LeadDeleteView(OrganisorAndLoginRequiredMixin, generic.DeleteView):# agent cannot delete an lead
	template_name = "lead_delete.html"

	def get_queryset(self):
		user = self.request.user	
		#organisor only can delete a lead
		return  Lead.objects.filter()

	def  get_success_url(self):
		return reverse("leads:lead-list")


class CategoryListView(LoginRequiredMixin, generic.ListView):
	template_name = "category/category_list.html"
	context_object_name = "category_list"

	def get_queryset(self):
		user = self.request.user
		if user.is_organisor:
			#if you are an organisor you see all leeds
			queryset= Category.objects.filter() 
		else:
			#agent only see leeds that are assigned to them
			queryset= Category.objects.filter()
			
		return queryset	

class CategoryDetailView(LoginRequiredMixin, generic.DetailView):
	template_name = "category/category_detail.html"
	context_object_name = "category"
	

	def get_queryset(self):
		queryset= Lead.object.filter(category = self.get_object()) #picks a specific category that we are working with
		return queryset			
	def get_queryset(self):
		user = self.request.user
		if user.is_organisor:
			#if you are an organisor you see all leeds
			queryset= Category.objects.filter() 
		else:
			#agent only see leeds that are assigned to them
			queryset= Category.objects.filter()
			
		return queryset

class LeadCategoryUpdateView(LoginRequiredMixin, generic.UpdateView):
	template_name = "category/lead_category_update.html"
	form_class = LeadCategoryUpdateForm


	def get_queryset(self):
		user = self.request.user
		if user.is_organisor:
			#if you are an organisor you see all leeds
			queryset= Lead.objects.filter()
			
		else:
			#agent only see leeds that are assigned to them
			queryset= Lead.objects.filter()
			#queryset= queryset.fliter(agent__user=user)
		return queryset
	
	def  get_success_url(self):
		return reverse("leads:lead-detail",kwargs={"pk": self.get_object().id})