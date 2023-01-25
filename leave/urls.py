from curses import can_change_color
from django.urls import path
from.views import (leave_creation,leaves_list,leaves_approved_list,leaves_view,approve_leave,cancel_leaves_list,unapprove_leave,
cancel_leave,uncancel_leave,leave_rejected_list,reject_leave,unreject_leave,view_my_leave_table)


app_name = "leave"

urlpatterns = [
    path('leave/apply', leave_creation, name='createleave'),
    path('leaves/pending/all/',leaves_list,name='leaveslist'),
    path('leaves/approved/all/',leaves_approved_list,name='approvedleaveslist'),
    path('leaves/cancel/all/',cancel_leaves_list,name='canceleaveslist'),
    path('leaves/all/view/<int:id>/',leaves_view,name='userleaveview'),
    path('leaves/view/table/',view_my_leave_table,name='staffleavetable'),
    path('leave/approve/<int:id>/',approve_leave,name='userleaveapprove'),
    path('leave/unapprove/<int:id>/',unapprove_leave,name='userleaveunapprove'),
    path('leave/cancel/<int:id>/',cancel_leave,name='userleavecancel'),
    path('leave/uncancel/<int:id>/',uncancel_leave,name='userleaveuncancel'),
    path('leaves/rejected/all/',leave_rejected_list,name='leavesrejected'),
    path('leave/reject/<int:id>/',reject_leave,name='reject'),
    path('leave/unreject/<int:id>/',unreject_leave,name='unreject'),
]