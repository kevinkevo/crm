from django.urls import path
from . import views
from .views import announcement_creation,announcement_all,AnnouncementDelete
app_name = 'announcements'

urlpatterns =[
    path('announcement/create', announcement_creation, name='announcement'),
    path('announcement/all/',announcement_all,name='announcementall'),
    path("announcement/<int:pk>/delete/", views.AnnouncementDelete.as_view(), name="announcementdelete"),
]
