from django.shortcuts import render
from django.shortcuts import render,redirect,get_object_or_404
from django.http import HttpResponse,HttpResponseRedirect
from django.conf import settings
from django.db.models import Q
import datetime
from django.core.mail import send_mail
from django.contrib import messages
from django.urls import reverse
from leave.models import Leave
from leave.forms import LeaveCreationForm
from leads.models import Lead
from django.conf import settings
User = settings.AUTH_USER_MODEL
from django.contrib.auth import get_user_model
from agents.mixins import OrganisorAndLoginRequiredMixin
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import generic
from django.views.generic.base import TemplateView
from django.views.generic.base import RedirectView
from django.views import View


User = get_user_model()

# Create your views here.
def leave_creation(request):
	if not request.user.is_authenticated:
		return redirect('registration:login')
	if request.method == 'POST':
		form = LeaveCreationForm(data = request.POST)
		if form.is_valid():
			instance = form.save(commit = False)
			user = request.user
			instance.user = user
			instance.save()


			# print(instance.defaultdays)
			messages.success(request,'Leave Request Sent,wait for Admins response',extra_tags = 'alert alert-success alert-dismissible show')
			return redirect('leave:createleave')

		messages.error(request,'failed to Request a Leave,please check entry dates',extra_tags = 'alert alert-warning alert-dismissible show')
		return redirect('leave:createleave')


	dataset = dict()
	form = LeaveCreationForm()
	dataset['form'] = form
	dataset['title'] = 'Apply for Leave'
	return render(request,'leave/create_leave.html',dataset)
	


def leaves_list(request):
	
	leaves = Leave.objects.all_pending_leaves()
	return render(request,'leave/leaves_recent.html',{'leave_list':leaves,'title':'leaves list - pending'})



def leaves_approved_list(request):
	if  (request.user.is_organisor ,request.user.is_agent and request.user.is_employee):
		return redirect('/')
	leaves = Leave.objects.all_approved_leaves() #approved leaves -> calling model manager method
	return render(request,'leave/leaves_approved.html',{'leave_list':leaves,'title':'approved leave list'})



def leaves_view(request,id):
	if not (request.user.is_authenticated):
		return redirect('/')

	leave = get_object_or_404(Leave, id = id)
	print(leave.user)
	lead = Lead.objects.filter()
	print(lead)
	return render(request,'leave/leave_detail_view.html',{'leave':leave,'lead':lead,'title':'{0}-{1} leave'.format(leave.user.username,leave.status)})









def approve_leave(request,id):
	if not (request.user.is_organisor and request.user.is_authenticated):
		return redirect('/')
	leave = get_object_or_404(Leave, id = id)
	user = leave.user
	lead =Lead.objects.filter()
	leave.approve_leave

	messages.error(request,'Leave successfully approved for {0}'.format(request.user.username),extra_tags = 'alert alert-success alert-dismissible show')
	return redirect('leave:userleaveview', id = id)


def cancel_leaves_list(request):
	#if not (request.user.is_organisor and request.user.is_authenticated):
		#return redirect('/')
	leaves = Leave.objects.all_cancel_leaves()
	return render(request,'leave/leaves_cancel.html',{'leave_list_cancel':leaves,'title':'Cancel leave list'})



def unapprove_leave(request,id):
	if not (request.user.is_authenticated and request.user.is_organisor):
		return redirect('/')
	leave = get_object_or_404(Leave, id = id)
	leave.unapprove_leave
	return redirect('leave:leaveslist') #redirect to unapproved list




def cancel_leave(request,id):
	if not (request.user.is_organisor and request.user.is_authenticated):
		return redirect('/')
	leave = get_object_or_404(Leave, id = id)
	leave.leaves_cancel

	messages.success(request,'Leave is canceled',extra_tags = 'alert alert-success alert-dismissible show')
	return redirect('leave:canceleaveslist')#work on redirecting to instance leave - detail view


# Current section -> here
def uncancel_leave(request,id):
	if not (request.user.is_organisor and request.user.is_authenticated):
		return redirect('/')
	leave = get_object_or_404(Leave, id = id)
	leave.status = 'pending'
	leave.is_approved = False
	leave.save()
	messages.success(request,'Leave is uncanceled,now in pending list',extra_tags = 'alert alert-success alert-dismissible show')
	return redirect('leave:canceleaveslist')#work on redirecting to instance leave - detail view



def leave_rejected_list(request):

	dataset = dict()
	leave = Leave.objects.all_rejected_leaves()

	dataset['leave_list_rejected'] = leave
	return render(request,'leave/rejected_leaves_list.html',dataset)



def reject_leave(request,id):
	dataset = dict()
	leave = get_object_or_404(Leave, id = id)
	leave.reject_leave
	messages.success(request,'Leave is rejected',extra_tags = 'alert alert-success alert-dismissible show')
	return redirect('leave:leavesrejected')

	# return HttpResponse(id)


def unreject_leave(request,id):
	leave = get_object_or_404(Leave, id = id)
	leave.status = 'pending'
	leave.is_approved = False
	leave.save()
	messages.success(request,'Leave is now in pending list ',extra_tags = 'alert alert-success alert-dismissible show')

	return redirect('leave:leavesrejected')



#  staffs leaves table user only
def view_my_leave_table(request,):
	# work on the logics
	if request.user.is_authenticated:
		user = request.user
		organisation = request.user.userprofile
		leaves = Leave.objects.filter(user=user)
		lead = Lead.objects.filter()
		print(leaves)
		dataset = dict()
		dataset['leave_list'] = leaves
		dataset['lead'] = lead
		dataset['title'] = 'Leaves List'
	else:
		return redirect('registration:login')
	return render(request,'leave/staff_leaves_table.html',dataset)









