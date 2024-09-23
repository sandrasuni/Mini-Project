from django.conf.urls import url
from student import views

urlpatterns=[
    url('student/',views.student),
    url('ms/',views.ms),
    url('update/(?P<idd>\w+)',views.update,name='upd'),
    url('delete/(?P<idd>\w+)',views.delete,name='del'),
    url('ve/',views.vstud)

]