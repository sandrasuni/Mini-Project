from django.conf.urls import url
from presence_log import views
from presence_log.views import get_student_details

urlpatterns = [
    url('presence_log/', views.presence),
    url('api/get_student_details/<str:mess_id>/', get_student_details, name='get_student_details'),
    # path('presence_log/', views.presence_log_view, name='presence_log'),
    url('api/get_student_details/<str:mess_id>/', views.get_student_details, name='get_student_details'),
    url('api/search_presence_log/<str:mess_id>/', views.search_presence_log, name='search_presence_log'),


    # url('ml/',views.ml),
    # url('stv/',views.stview),
    # url('vl/',views.vleave),
    # url('approve/(?P<idd>\w+)', views.approve_leave_request, name='approve'),
    # url('reject/(?P<idd>\w+)', views.reject_leave_request, name='reject'),
] 