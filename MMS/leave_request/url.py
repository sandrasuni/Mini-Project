from django.conf.urls import url
from leave_request import views

urlpatterns = [
    url('lr/', views.leave),
    url('ml/',views.ml),
    url('stv/',views.stview),
    url('vl/',views.vleave),
    url('ds/',views.students_present),
    url('approve/(?P<idd>\w+)', views.approve_leave_request, name='approve'),
    url('reject/(?P<idd>\w+)', views.reject_leave_request, name='reject'),
] 