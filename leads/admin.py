from django.contrib import admin
from .models import Agent, Category, Lead, User, UserProfile
from leave.models import Leave
from leads.models import Employee,Department,Attendance,Kin
from leads.models import Announcement
from django.contrib import admin

# Register your models here.

admin.site.register(Agent)
admin.site.register(Lead)
admin.site.register(Category)
admin.site.register(Leave)
admin.site.register(Announcement)
admin.site.register([Employee,Department,Attendance,Kin])
admin.site.register(UserProfile)
admin.site.register(User)



#@admin.register(Announcement)
#class AnnouncementAdmin(admin.ModelAdmin):
    #list_display = ('body', 'level', 'display')
