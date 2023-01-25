from django.contrib.auth import get_user_model
from django import forms
from leads.models import Announcement
User = get_user_model()


class AnnouncementForm(forms.ModelForm):
	class Meta:
		model = Announcement
		fields = (
			'body',
			'display',
			'level',
			
			
		)